from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
requirements = []
for line in (ROOT / "requirements.txt").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    requirements.append(line)

setup(
    name="wagtail-shopify",
    version="0.2.0",
    description="Shopify embedded CMS backend (Django + Wagtail + Puck SPA)",
    packages=find_packages(
        exclude=("frontend", "scripts", "bin", "docs", "tests"),
    ),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.11",
)
