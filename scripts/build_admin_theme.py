#!/usr/bin/env python3
"""Generate the Wagtail admin stylesheet for the PLT "cheesecake" theme.

Reads the colour and font tokens of ``plt-design-system`` and writes
``admin_theme/static/admin_theme/css/cheesecake-admin.css``, which overrides
Wagtail's ``--w-color-*`` / ``--w-font-sans`` custom properties (see "Custom
user interface colors" in the Wagtail docs). Only the standard library is used.

Usage::

    python scripts/build_admin_theme.py --design-system ../plt-design-system
    python scripts/build_admin_theme.py --design-system ../plt-design-system --check

Colours are applied to the light theme only: cheesecake has no dark variant, so
``.w-theme-dark`` keeps Wagtail's own palette. The script exits non-zero when a
mapped pair would fall below WCAG AA, rather than emitting an inaccessible UI.
"""

from __future__ import annotations

import argparse
import colorsys
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME_DIR = ROOT / "admin_theme"
OUTPUT = THEME_DIR / "static" / "admin_theme" / "css" / "cheesecake-admin.css"
SHA_FILE = THEME_DIR / "DESIGN_SYSTEM_SHA"
SRC = Path("packages/design-system/src")

AA_TEXT = 4.5
STATUS_MIN_L = 0.45  # oklch lightness floor for status accents
STATUS_MIN_C = 0.15  # oklch chroma floor for status accents

# Wagtail status family -> (design-system token, base shade variable name).
# The base shade is the one the other shades are derived from.
STATUS = {
    "info": ("info", "125"),
    "positive": ("success", "100"),
    "warning": ("warning", "100"),
    "critical": ("error", "200"),
}

FONT_FACES = (
    # (file, weight, unicode-range)
    ("atkinson-hyperlegible-latin-400-normal.woff2", 400,
     "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
     "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("atkinson-hyperlegible-latin-700-normal.woff2", 700,
     "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
     "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("atkinson-hyperlegible-latin-ext-400-normal.woff2", 400,
     "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
     "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,"
     "U+2113,U+2C60-2C7F,U+A720-A7FF"),
    ("atkinson-hyperlegible-latin-ext-700-normal.woff2", 700,
     "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
     "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,"
     "U+2113,U+2C60-2C7F,U+A720-A7FF"),
)


# --------------------------------------------------------------------------
# Colour maths
# --------------------------------------------------------------------------

def _gamma(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklch_to_linear(lightness: float, chroma: float, hue: float) -> tuple[float, float, float]:
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l_ = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )


def oklch_to_rgb(lightness: float, chroma: float, hue: float) -> tuple[float, float, float]:
    """oklch -> sRGB in 0..1, reducing chroma until the colour is in gamut."""
    while True:
        lin = oklch_to_linear(lightness, chroma, hue)
        if all(-1e-4 <= c <= 1 + 1e-4 for c in lin) or chroma <= 0:
            return tuple(min(1.0, max(0.0, _gamma(max(0.0, c)))) for c in lin)  # type: ignore[return-value]
        chroma -= 0.002


def rgb_to_oklch(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_linear(c) for c in rgb)
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    lab_l = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    lab_a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    lab_b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return lab_l, math.hypot(lab_a, lab_b), math.degrees(math.atan2(lab_b, lab_a)) % 360


def parse_color(value: str) -> tuple[float, float, float]:
    value = value.strip()
    if value.startswith("#"):
        digits = value[1:]
        if len(digits) == 3:
            digits = "".join(ch * 2 for ch in digits)
        return tuple(int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]
    match = re.fullmatch(r"oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s*\)", value)
    if match:
        lightness, chroma, hue = match.groups()
        return oklch_to_rgb(float(lightness) / 100, float(chroma), float(hue))
    raise ValueError(f"Unsupported colour value: {value!r}")


def to_hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02X}" for c in rgb)


def mix(a: tuple[float, float, float], b: tuple[float, float, float], amount: float):
    """Mix ``amount`` of ``b`` into ``a`` (sRGB, like color-mix(in srgb))."""
    return tuple(x * (1 - amount) + y * amount for x, y in zip(a, b))


def luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def hsl_parts(rgb: tuple[float, float, float]) -> tuple[str, str, str]:
    hue, light, sat = colorsys.rgb_to_hls(*rgb)
    return f"{hue * 360:.1f}", f"{sat * 100:.1f}%", f"{light * 100:.1f}%"


# --------------------------------------------------------------------------
# Tokens
# --------------------------------------------------------------------------

def read_tokens(design_system: Path) -> tuple[dict[str, tuple[float, float, float]], str]:
    colors_css = (design_system / SRC / "tokens" / "colors.css").read_text()
    typography_css = (design_system / SRC / "typography.css").read_text()

    colors = {}
    for name, value in re.findall(r"--plt-color-([a-z0-9-]+):\s*([^;]+);", colors_css):
        if value.startswith(("#", "oklch(")):
            colors[name] = parse_color(value)

    font = re.search(r"--plt-font-body:\s*([^;]+);", typography_css)
    if not font:
        raise SystemExit("--plt-font-body not found in typography.css")
    return colors, font.group(1).strip()


def status_accent(content: tuple[float, float, float], backgrounds) -> tuple[float, float, float]:
    """Wagtail's status shades are saturated mid-tones, while cheesecake's
    ``*-content`` tokens are near-black. Keep the token hue and move to a mid-tone
    that still reaches AA on every background it will be shown on."""
    lightness, chroma, hue = rgb_to_oklch(content)
    lightness = max(lightness, STATUS_MIN_L)
    chroma = max(chroma, STATUS_MIN_C)
    while lightness > 0.2:
        rgb = oklch_to_rgb(lightness, chroma, hue)
        if all(contrast(rgb, bg) >= AA_TEXT for bg in backgrounds):
            return rgb
        lightness -= 0.01
    raise SystemExit("Could not find an AA-compliant status accent")


# --------------------------------------------------------------------------
# Stylesheet
# --------------------------------------------------------------------------

def build_palette(colors: dict[str, tuple[float, float, float]]) -> tuple[dict[str, str], list[str]]:
    """Return light-theme variables and the list of contrast checks performed."""
    required = [
        "base-100", "base-200", "base-content", "primary", "accent", "accent-content",
        *(f"{token}" for token, _ in STATUS.values()),
        *(f"{token}-content" for token, _ in STATUS.values()),
    ]
    missing = [name for name in required if name not in colors]
    if missing:
        raise SystemExit(f"Missing design-system colours: {', '.join(missing)}")

    page = colors["base-100"]
    white = (1.0, 1.0, 1.0)
    variables: dict[str, str] = {}
    checks: list[str] = []

    def require(label: str, fg, bg, minimum: float = AA_TEXT) -> None:
        ratio = contrast(fg, bg)
        checks.append(f"{label}: {ratio:.2f}:1")
        if ratio < minimum:
            raise SystemExit(f"Contrast too low for {label}: {ratio:.2f}:1 (< {minimum}:1)")

    # Brand. In Wagtail, `primary` is the sidebar and `secondary` drives buttons and links.
    primary = colors["primary"]
    hue, sat, light = hsl_parts(primary)
    variables.update({
        "--w-color-primary-hue": hue,
        "--w-color-primary-saturation": sat,
        "--w-color-primary-lightness": light,
    })
    require("sidebar text (white 80%) on primary", mix(primary, white, 0.8), primary)

    accent = colors["accent"]
    hue, sat, light = hsl_parts(accent)
    variables.update({
        "--w-color-secondary-hue": hue,
        "--w-color-secondary-saturation": sat,
        "--w-color-secondary-lightness": light,
    })
    # secondary-50 is derived as lightness + 72.2%; keep it a visible tint, not pure white.
    if float(light.rstrip("%")) + 72.2 > 96:
        variables["--w-color-secondary-50-lightness"] = "95%"
    require("link (accent) on page", accent, page)
    require("button text on accent", colors["accent-content"], accent)

    # Surfaces and text (light theme only).
    content = colors["base-content"]
    variables.update({
        "--w-color-surface-page": to_hex(page),
        "--w-color-surface-header": to_hex(mix(page, content, 0.06)),
        "--w-color-surface-field-inactive": to_hex(mix(page, content, 0.06)),
        "--w-color-surface-dashboard-panel": to_hex(colors["base-200"]),
        "--w-color-text-context": to_hex(content),
        "--w-color-text-button": to_hex(colors["accent-content"]),
    })
    require("body text on page", content, page)

    # Status families.
    for family, (token, shade) in STATUS.items():
        pastel = colors[token]
        accent_rgb = status_accent(colors[f"{token}-content"], (page, pastel))
        hue, sat, light = hsl_parts(accent_rgb)
        base = f"--w-color-{family}-{shade}"
        variables.update({
            f"{base}-hue": hue,
            f"{base}-saturation": sat,
            f"{base}-lightness": light,
            f"--w-color-{family}-50": to_hex(pastel),
        })
        require(f"{family} accent on page", accent_rgb, page)
        require(f"{family} accent on pastel", accent_rgb, pastel)
        if family == "critical":
            require("button text on critical", colors["accent-content"], accent_rgb)
        if family == "info":
            variables["--w-color-text-status-label"] = f"var({base})"

    return variables, checks


def declarations(variables: dict[str, str], indent: str = "  ") -> str:
    return "\n".join(f"{indent}{name}: {value};" for name, value in variables.items())


def font_faces() -> str:
    blocks = []
    for filename, weight, unicode_range in FONT_FACES:
        blocks.append(
            "@font-face {\n"
            '  font-family: "Atkinson Hyperlegible";\n'
            "  font-style: normal;\n"
            f"  font-weight: {weight};\n"
            "  font-display: swap;\n"
            f'  src: url("../fonts/{filename}") format("woff2");\n'
            f"  unicode-range: {unicode_range};\n"
            "}"
        )
    return "\n\n".join(blocks)


def render(colors, font_stack: str, sha: str) -> tuple[str, list[str]]:
    variables, checks = build_palette(colors)
    body = declarations(variables)
    nested = declarations(variables, indent="    ")
    css = f"""/*
 * GENERATED FILE - DO NOT EDIT.
 * Source: plt-design-system `cheesecake` theme @ {sha}
 * Regenerate: make admin-theme DESIGN_SYSTEM=../plt-design-system
 *
 * Cheesecake is light-only, so the palette is applied to the light theme and
 * to the system theme when the OS prefers light. `.w-theme-dark` is untouched.
 */

{font_faces()}

:root {{
  --w-font-sans: {font_stack};
}}

.w-theme-light {{
{body}
}}

@media (prefers-color-scheme: light) {{
  .w-theme-system {{
{nested}
  }}
}}
"""
    return css, checks


def design_system_sha(design_system: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(design_system), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design-system", required=True, type=Path,
                        help="path to a checkout of plt-design-system")
    parser.add_argument("--check", action="store_true",
                        help="fail if the committed stylesheet differs, write nothing")
    args = parser.parse_args()

    design_system = args.design_system.resolve()
    colors, font_stack = read_tokens(design_system)
    sha = design_system_sha(design_system)
    css, checks = render(colors, font_stack, sha)

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != css:
            print(f"{OUTPUT.relative_to(ROOT)} is out of date; run `make admin-theme`.", file=sys.stderr)
            return 1
        print("cheesecake-admin.css is up to date.")
        return 0

    OUTPUT.write_text(css)
    SHA_FILE.write_text(sha + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} (design system {sha[:10]})")
    for line in checks:
        print(f"  ok  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
