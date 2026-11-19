# Quick start (≈5 minutes)

> **Translator:** EN SoT [`docs/quick-start.md`](../../quick-start.md). Keep fences/paths/commands literal. Glossary: [`docs/i18n/glossary.yaml`](../../i18n/glossary.yaml).

## What this repo is / is not

| Is | Is not |
| :--- | :--- |
| Two Agent Skills (`evidence-bank`, `cv-creation`) + docs, fixtures, scripts | Your private career tree (identity, evidence, applications) |
| Validators / export helpers you run locally | A hosted CV SaaS |

Career facts stay in a separate career project. This repo ships skills and fixtures only.

## Pick a path

| Path | When | Open | Recommendation |
| :--- | :--- | :--- | :--- |
| **Full** | Agent Skills client; want reliable Python deps | `prompts/<lang>/install-full.md` | **Recommended** for first install when you want `make smoke` / validators. |
| **Lite** | Same client; ask before package installs | `prompts/<lang>/install-lite.md` | Use when package installs must wait for your OK. |
| **Web chat** | No Agent Skills client | [`web-chat.md`](web-chat.md) | Only when you cannot install skill folders. |

Refresh already-installed skills: `prompts/<lang>/update.md`.

## 5-minute smoke after clone

From repo root (run `make deps` first if `import yaml` fails):

```bash
make smoke
```

**Privacy:** [`privacy-security.md`](privacy-security.md) · full EN [`SECURITY.md`](../../../SECURITY.md).

**Languages:** [English](../../quick-start.md) · [Français](../fr/quick-start.md) · [العربية](../ar/quick-start.md)
