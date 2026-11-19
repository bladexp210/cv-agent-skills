# User-locale status

English install/use docs at repo root (`README.md`, `docs/quick-start.md`, `docs/web-chat.md`, `SECURITY.md`, `prompts/*.md`) remain SoT until a locale is marked `current`.

| Locale | Status | EN pin | Checked | Owner | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `en` | SoT (pin) | `v0.10.1` | 2026-11-19 | foundation | Canonical EN corpus + `locales/en.yaml`; path-copy situation/end-result refresh |
| `fr` | current | `v0.10.1` | 2026-11-19 | french | Full corpus + `fr.yaml`; path-copy refresh synced with EN |
| `ar` | current | `v0.10.1` | 2026-11-19 | arabic | Full corpus + `ar.yaml`; RTL notes; path-copy refresh synced with EN |

## Sync rule

When any EN corpus file or `locales/en.yaml` changes:

1. Update `en` row `EN pin` to the commit (or content hash) that owns the change.
2. Set every non-EN locale to `stale` until re-checked.
3. Do not mark a locale `current` while stale.

## Glossary

`docs/i18n/glossary.yaml` — FR and AR columns filled for critical terms (foundation).
