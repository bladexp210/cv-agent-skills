# Quick start (≈5 minutes)

> **Translator:** EN SoT [`docs/quick-start.md`](../../quick-start.md). Keep fences/paths/commands literal. Glossary: [`docs/i18n/glossary.yaml`](../../i18n/glossary.yaml).

## What this repo is / is not

| Is | Is not |
| :--- | :--- |
| Two Agent Skills (`evidence-bank`, `cv-creation`) + docs, fixtures, scripts | Your private career tree (identity, evidence, applications) |
| Validators / export helpers you run locally | A hosted CV SaaS |

Career facts stay in a separate career project. This repo ships skills and fixtures only.

## Pick a path

| Path | Situation | End result | Open | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Full** | Agent Skills client **and** willing to install Python, libraries, and related developer tools | Skills installed + **repeatable** validate/export via local scripts | `prompts/<lang>/install-full.md` | **Prefer Full** when you have a client and can install Python. |
| **Lite** | Agent Skills client **but** cannot or will not install that Python stack | Skills load in the agent; artifacts mainly from the agent (optional polish in Word / Docs / LibreOffice). Weaker script guarantees | `prompts/<lang>/install-lite.md` | **Prefer Lite** when you have a client but refuse or cannot install Python. |
| **Web chat** | **No** Agent Skills client — browser chatbot only | Structured mega-prompt + save files outside the chat | [`web-chat.md`](web-chat.md) | Use Web **only** when you have no skills client. |

Refresh already-installed skills: `prompts/<lang>/update.md`.

## 5-minute smoke after clone

From repo root (run `make deps` first if `import yaml` fails):

```bash
make smoke
```

**Privacy:** [`privacy-security.md`](privacy-security.md) · full EN [`SECURITY.md`](../../../SECURITY.md).

**Languages:** [English](../../quick-start.md) · [Français](../fr/quick-start.md) · [العربية](../ar/quick-start.md)
