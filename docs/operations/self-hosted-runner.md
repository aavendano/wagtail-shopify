# Self-hosted runner — wagtail-shopify (`wagtail-runner-01`)

| Parameter | Value |
|---|---|
| Scope | Repository `aavendano/wagtail-shopify` |
| Name | `wagtail-runner-01` |
| Labels | `self-hosted`, `linux`, `x64`, `wagtail-ci` |
| Host | VPS `hetzner-dev` (shared host with `cms-runner-01`, separate install dir) |
| User | `github-runner` |
| Dir | `/opt/github-runners/wagtail-runner-01` |
| Agent | `2.338.0` (version advertised to this repo at install) |

## Security (public repository)

This repository is **public**. Fork pull requests must **not** run on the
persistent runner. Workflows keep `ubuntu-latest` when
`github.event.pull_request.head.repo.fork` is true; same-repo pushes/PRs and
`workflow_dispatch` use `wagtail-ci`.

## Install

```bash
sudo bash /tmp/install-wagtail-runner-root.sh   # Root 1
# agent injects registration token, then:
sudo bash /tmp/wagtail-runner-configure-and-svc.sh  # Root 2
```

Does not replace or stop `cms-runner-01`.


## Verification evidence

- Runner Online: Settings → Actions → Runners (`wagtail-runner-01`, labels `wagtail-ci`)
- systemd: `actions.runner.aavendano-wagtail-shopify.wagtail-runner-01.service` (enabled, active)
- Successful run: https://github.com/aavendano/wagtail-shopify/actions/runs/39830151567 (`content-validate`, runner `wagtail-runner-01`)
- `cms-runner-01` remains Online for `shopify-django-md-cms` (separate install)
