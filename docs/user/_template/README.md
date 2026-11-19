# CV Agent Skills — user docs (`<lang>`)

> **Translator:** copy this folder to `docs/user/<lang>/`. Translate prose; keep paths, commands, and skill ids literal. EN SoT: root [`README.md`](../../../README.md). Glossary: [`docs/i18n/glossary.yaml`](../../i18n/glossary.yaml).

**What this is:** installable [Agent Skills](https://agentskills.io/home) for a private facts bank (`evidence-bank`) and a per-job CV pipeline (`cv-creation`).

**Next:** open [`quick-start.md`](quick-start.md) (≈5 minutes), or pick an install prompt below.

| Situation | End result | Open | Recommendation |
| :--- | :--- | :--- | :--- |
| Agent Skills client **and** willing to install Python + libraries + related tools (first time) | Skills installed + **repeatable** validate/export via local scripts | [`../../../prompts/_template/install-full.md`](../../../prompts/_template/install-full.md) → after copy: `prompts/<lang>/install-full.md` | **Prefer Full** when the client and Python stack are both available. |
| Agent Skills client **but** cannot or will not install that Python stack (first time) | Skills load in the agent; artifacts mainly from the agent (optional polish in Word / Docs / LibreOffice). Weaker script guarantees | `prompts/<lang>/install-lite.md` | **Prefer Lite** when you have a client but refuse or cannot install Python. |
| **No** Agent Skills client — browser chatbot only | Structured mega-prompt + save files outside the chat | [`web-chat.md`](web-chat.md) | Use Web chat **only** when you have no skills client. |

**Languages:** [English (SoT)](../../../README.md) · [Français](../fr/README.md) · [العربية](../ar/README.md)

**Privacy (short):** [`privacy-security.md`](privacy-security.md) — full matrix: [`SECURITY.md`](../../../SECURITY.md).

**For maintainers:** [`docs/README.md`](../../README.md) (English).
