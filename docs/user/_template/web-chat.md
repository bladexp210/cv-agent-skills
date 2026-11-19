# Web chat path (no Agent Skills client)

> **Translator:** EN SoT [`docs/web-chat.md`](../../web-chat.md). Keep mega-prompt fences and paths literal. Glossary: [`docs/i18n/glossary.yaml`](../../i18n/glossary.yaml).

A guided CV system in chat — better than a one-shot “write my resume” prompt. You keep a small reusable facts folder and update it as you go.

**Situation:** you have **no** Agent Skills client — “AI” for you means a browser chatbot (ChatGPT, Claude.ai, Gemini, …).  
**End result:** a **structured** mega-prompt + discipline to save files outside the chat — better than ad-hoc social-media prompt tricks.

| Situation | End result | Use | Recommendation |
| :--- | :--- | :--- | :--- |
| Agent Skills client **and** willing to install Python + libraries + related tools | Skills installed + **repeatable** validate/export via local scripts | `prompts/<lang>/install-full.md` | **Prefer Full** when the client and Python stack are both available. |
| Agent Skills client **but** cannot or will not install that Python stack | Skills load in the agent; artifacts mainly from the agent. Weaker script guarantees | `prompts/<lang>/install-lite.md` | **Prefer Lite** when you have a client but refuse or cannot install Python. |
| **No** Agent Skills client — browser chatbot only | Structured mega-prompt + save files outside the chat | **This page** | Use Web chat **only** when skill install is impossible. |

## Keep a `career/` folder

Web chat has no skill install and no automatic scripts. Save proposed facts and drafts into real files outside the chat.

**Privacy:** [`privacy-security.md`](privacy-security.md) · full EN [`SECURITY.md`](../../../SECURITY.md).

**Languages:** [English](../../web-chat.md) · [Français](../fr/web-chat.md) · [العربية](../ar/web-chat.md)

---

<!-- Translator: paste/adapt the EN mega-prompt and remaining sections from docs/web-chat.md here. Do not translate paths, skill ids, or fenced commands. -->
