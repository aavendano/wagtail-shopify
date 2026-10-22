# ADR 0002: Tenancy deploy-per-shop + ShopMembership

## Status

Accepted

## Context

After the `core` → `shopify_admin` / `shopify_config` split (ADR 0001), shop
resolution still used silent `ShopConfig.objects.first()` on sync paths,
management commands, and admin views. The MD CMS
(`shopify-django-md-cms`) already had a fail-closed tenancy contract
(`content/tenancy.py`, `accounts/membership.py`, ADR 0017) that we want to
reuse logically without adopting SaaS multi-tree editorial isolation.

## Decision

1. **Parity 1A (logic, not editorial rows).** Port normalize/session/membership
   helpers into `shopify_config` (`tenancy.py`, `membership.py`,
   `ShopMembership`). Do **not** add `shop` to Wagtail page models, do **not**
   create Site-per-shop, do **not** port `ShopGitBinding` / GitHub App.

2. **Deploy-per-shop.** One Wagtail process/DB = one Shopify merchant. Sync
   without an HTTP request uses `resolve_sole_installed_shop()` (exactly one
   `ShopConfig`; error if 0 or N>1). Management commands accept `--shop` and
   may fall back to `SHOPIFY_PUBLICATION_SHOP` then sole-shop.

3. **Session + membership.** App Home sets `SESSION_SHOP` after the offline
   token lifecycle and bootstraps admin membership from staff claims when
   present. CMS session auth (`SessionEditorAuth`) requires membership (or
   superuser) for the session/sole shop. `GET/POST /api/v1/session-shop/`
   lists and selects shops. ApiKey remains deploy-global (follow-up: per-shop
   keys).

4. **AUTH_USER_MODEL unchanged.** `ShopMembership.user` FKs the default Django
   user. Installer bootstrap marks users `is_staff=True`.

5. **Uninstall.** Deletes memberships for the shop, then `ShopConfig`.

6. **Backfill.** Migration grants `admin` membership to existing `is_staff`
   users when exactly one `ShopConfig` exists.

## Consequences

- Call sites must not use silent `objects.first()` for tenant resolution.
- Misconfigured installs with multiple `ShopConfig` rows fail closed until
  `--shop` is passed or extras are removed.
- Editors without membership cannot use the CMS SPA until App Home claims
  bootstrap or an operator assigns membership in Django Admin.

## Related

- ADR 0001 — core app split
- MD CMS ADR 0017 — ShopMembership (source pattern)
