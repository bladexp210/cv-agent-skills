# CV Agent Skills

Open [Agent Skills](https://agentskills.io/home) for building and tailoring a CV.  
**Agent Skills** = installable skill folders that an AI client can load (not a normal web chat paste).

**Who this is for:** people who use an Agent Skills client and keep career facts in their own private project.

![Evidence bank to CV pipeline](docs/assets/visuals/hero-readme.jpeg)

**Two skills:**

| Skill | Job |
| :--- | :--- |
| <img src="docs/assets/visuals/icon-evidence-bank.jpeg" alt="" width="40" height="40" /> `evidence-bank` | Maintain a de-styled facts bank (YAML). Validate before you trust it. |
| <img src="docs/assets/visuals/icon-cv-creation.jpeg" alt="" width="40" height="40" /> `cv-creation` | Run a per-application CV pipeline (match job → draft → export). |

```mermaid
flowchart LR
  bank[evidence-bank] --> pipe[cv-creation]
  pipe --> out[export]
```

**Private career data lives elsewhere.** This repo ships skills, docs, and fixtures only. Put real identity, evidence YAML, and applications in your own career tree.

### Privacy

Career PII stays in your private career tree — not in this repo. Bundled scripts use local files only and never phone home (see [Security](SECURITY.md)). Treat job descriptions pasted into agents as untrusted text (prompt-injection risk). Agent chats may leave the machine per your client’s policy.

**Security:** [SECURITY.md](SECURITY.md) — per-script reads / writes / network / exits.

---

## Dependencies (full path)

Use these when you want reliable scripts (validate, export).

| File | Packages | When |
| :--- | :--- | :--- |
| [`requirements.txt`](requirements.txt) | `pyyaml` | YAML validate / views / most bank scripts |
| [`requirements-export.txt`](requirements-export.txt) | `python-docx`, `weasyprint` | DOCX / PDF export (WeasyPrint may need OS libraries) |

### Full vs Lite

| | Full | Lite |
| :--- | :--- | :--- |
| Install skill folders | Yes | Yes |
| Install Python packages | When a step needs them; ask before heavy or surprising installs | Only if you say yes |
| Scripts | Prefer bundled scripts; install deps so they run | Use scripts only if they already run; otherwise adapt |
| Promise | Stronger integrity via validators and export scripts | Honest gaps; quality tracks what already works on your machine |

---

## Install

Pick one path. Copy the paste-prompt into a new agent chat in your **career** project (skills repo need not be open).

Default skill source is the public GitHub repo:  
https://github.com/bladexp210/cv-agent-skills  
(Use a local checkout only if you explicitly tell the agent that path.)

```mermaid
flowchart TD
  q{Agent Skills client?}
  q -->|yes first| full[Install Full]
  q -->|yes first| lite[Install Lite]
  q -->|yes already| upd[Update skills]
  q -->|no| web[Web chat page]
```

| You want… | Open |
| :--- | :--- |
| Skills + reliable Python deps (first time) | [`prompts/install-full.md`](prompts/install-full.md) |
| Skills only; ask before any package install (first time) | [`prompts/install-lite.md`](prompts/install-lite.md) |
| Refresh skills already installed (keep career data) | [`prompts/update.md`](prompts/update.md) |

The agent should use **its own** skill-install location (see that product’s docs). Do not assume one vendor path.

---

## Web chat (no skills client)

Normal web chat cannot install Agent Skills folders from disk. If you use ChatGPT, Claude.ai, Gemini, or similar, follow the guided path in [`docs/web-chat.md`](docs/web-chat.md).

When an Agent Skills client is available, prefer **Full** or **Lite** above — those paths load the skills and scripts for you.

---

## Quick smoke (full path)

After Full install (or when PyYAML is already available):

```bash
python skills/evidence-bank/scripts/validate_evidence.py \
  skills/evidence-bank/assets/fixtures/ok.yaml
```

Expect a clean pass on the fixture. Real career YAML stays outside this repo.

Evidence contract and samples:

| What | Path |
| :--- | :--- |
| Prose schema | [`skills/evidence-bank/references/evidence-schema.md`](skills/evidence-bank/references/evidence-schema.md) |
| Machine schema | [`skills/evidence-bank/assets/evidence.schema.json`](skills/evidence-bank/assets/evidence.schema.json) |
| Pass fixture | [`skills/evidence-bank/assets/fixtures/ok.yaml`](skills/evidence-bank/assets/fixtures/ok.yaml) |
| Fail fixture (negative) | [`skills/evidence-bank/assets/fixtures/bad-missing-source.yaml`](skills/evidence-bank/assets/fixtures/bad-missing-source.yaml) |

---

## Builders / maintainers

Repo map (design, architecture, contract, agent load order): [`docs/README.md`](docs/README.md).

---

## License

MIT — see [`LICENSE`](LICENSE).
