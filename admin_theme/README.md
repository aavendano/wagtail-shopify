# admin_theme — PLT "cheesecake" theme and branding for the Wagtail admin

Skins the Wagtail admin with the `cheesecake` theme of
[`plt-design-system`](https://github.com/aavendano/plt-design-system), using the
mechanism documented in Wagtail's "Custom user interface colors": override the
`--w-color-*` / `--w-font-sans` custom properties and inject the stylesheet with the
`insert_global_admin_css` hook (`wagtail_hooks.py`). The colors and fonts need no template
override; only the branding (below) overrides three admin templates, through their documented blocks.

## What is mapped

| Wagtail | cheesecake token |
|---|---|
| `primary` (sidebar) | `--plt-color-primary` `#533278` |
| `secondary` (buttons, links) | `--plt-color-accent` teal `#0C7489` |
| page / panel surfaces | `base-100` cream, `base-200` |
| body text | `base-content` |
| `info` / `positive` / `warning` / `critical` `-50` | pastel `info` / `success` / `warning` / `error` |
| status accents | hue of the `*-content` token, set to a mid-tone that reaches WCAG AA |
| `--w-font-sans` | `--plt-font-body` (Atkinson Hyperlegible, self-hosted) |

Not used: hot pink `--plt-color-secondary` (`#F4436C`, 3.35:1 on cream, below AA for text),
Wagtail's focus colour (kept at Wagtail's tested default so it stays visible on both the
purple sidebar and the cream page), and cheesecake's hard shadows, radii and uppercase
headings (they would need component-level overrides).

Cheesecake has no dark variant, so the palette applies to `.w-theme-light` and to
`.w-theme-system` when the OS prefers light. `.w-theme-dark` keeps Wagtail's own colours.

## Regenerating

`static/admin_theme/css/cheesecake-admin.css` is generated and committed; do not edit it.
The design system is consumed by git SHA, so regenerate when you move to a new commit:

```bash
git -C ../plt-design-system checkout <sha>
make admin-theme DESIGN_SYSTEM=../plt-design-system   # writes the CSS and DESIGN_SYSTEM_SHA
make admin-theme-check                                 # fails if the committed CSS is stale
```

The generator needs only Python's standard library. It exits with an error if a mapped pair
(body text, links, button text, sidebar text, status accents) falls below 4.5:1, so a token
change cannot silently produce an inaccessible admin.

## Branding

PlayLoveToys logo, favicon and titles, through Wagtail's documented template blocks
(`templates/wagtailadmin/{base,login,admin_base}.html`; this app must stay before
`wagtail.admin` in `INSTALLED_APPS`). `static/admin_theme/css/branding.css` is hand-written.

| Where | Asset |
|---|---|
| Sidebar | `img/plt-logo.svg`, white wordmark, works on the purple sidebar and the dark theme |
| Login, light theme | `img/plt-logo-on-light.svg` |
| Login, dark theme / OS dark | `img/plt-logo.svg` (`branding.css` switches on `.w-theme-dark` and `.w-theme-system`) |
| Favicon | `img/favicon-32x32.png` |
| Browser title, login heading | "PlayLoveToys" / "Sign in to PlayLoveToys" |

Sources: `plt-logo.svg` and the favicon are the files published on the PlayLoveToys store
(`PlayLoveToys-Logo.svg`, `favicon-playlovetoys-32x32.png`). `plt-logo-on-light.svg` is a derived
copy with the five near-white fills (`#FEFEFE`, `#FDFDFD`, `#F6F6F6`) recoloured to the brand
purple `#533278`, because the original's white wordmark is invisible on the cream login card.
Replace it with official artwork if one exists. Logos are exempt from WCAG contrast rules.

Not changed: the dashboard heading still reads `WAGTAIL_SITE_NAME` ("Wagtail Shopify"), and the
Wagtail 404 page keeps its own logo.

## Deployment

The stylesheet and fonts are ordinary static files (`STORAGES` uses Django's plain
`StaticFilesStorage`, so the CSS can reference `../fonts/` relatively). Production must run
`python manage.py collectstatic --noinput` (the README's `scripts/bootstrap_app.sh` step) and
serve `STATIC_ROOT` under `/static/`; Django only does that itself when `DEBUG` is on.

Checked locally: `collectstatic` copies `cheesecake-admin.css` and the four `.woff2` files, and
`../fonts/...` resolves from the CSS URL.

Example Caddy block (**illustrative, not validated against the real Caddyfile**; adjust the path
to your `STATIC_ROOT`):

```caddyfile
cms.example.com {
    handle_path /static/* {
        root * /path/to/backend/staticfiles
        header Cache-Control "public, max-age=31536000"
        file_server
    }
    reverse_proxy 127.0.0.1:8083
}
```

The CSS link carries a `?v=<hash>` (Wagtail's `versioned_static`), so a long cache lifetime is
safe for the stylesheet; the fonts have stable names and change only when replaced.

After deploying, confirm both files are reachable:

```bash
curl -I https://<cms-host>/static/admin_theme/css/cheesecake-admin.css
curl -I https://<cms-host>/static/admin_theme/fonts/atkinson-hyperlegible-latin-400-normal.woff2
```

Font files are Atkinson Hyperlegible (SIL OFL 1.1, from `@fontsource/atkinson-hyperlegible`
5.3.0); the licence is in `static/admin_theme/fonts/`.
