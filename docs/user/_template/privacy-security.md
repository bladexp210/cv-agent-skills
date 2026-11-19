# Privacy and security (user slice)

> **Translator:** Short user-facing slice of EN [`SECURITY.md`](../../../SECURITY.md). Do **not** soften warnings. Link the full English matrix for script I/O details.

## Standing rules

- **Career PII lives outside this repo.** Real identity, evidence YAML, and applications stay in your private career tree. This repo ships skills, docs, and fixtures only.
- **Scripts never phone home.** Bundled scripts use local filesystem I/O only. No HTTP clients, sockets, or telemetry from script code.
- **Agent chats are separate.** Pasting career text or job descriptions into an Agent Skills client may leave the machine per that product’s policy. Treat untrusted job-description text as prompt-injection risk.

## What to do next

1. Keep private career data in your own career project — not in this skills pack.
2. Read the full script matrix when you need exact reads / writes / exits: [`SECURITY.md`](../../../SECURITY.md) (English).
3. Report vulnerabilities via GitHub Security Advisories on this repository (private disclosure) — see EN `SECURITY.md`.

**Languages:** [English SECURITY](../../../SECURITY.md) · [Français](../fr/privacy-security.md) · [العربية](../ar/privacy-security.md)
