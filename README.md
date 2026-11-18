# CV Agent Skills

Open [Agent Skills](https://agentskills.io/home) for building and tailoring a CV.  
**Agent Skills** = installable skill folders that an AI client can load (not a normal web chat paste).

**Who this is for:** people who use an Agent Skills client and keep career facts in their own private project.

**Two skills:**

| Skill | Job |
| :--- | :--- |
| `evidence-bank` | Maintain a de-styled facts bank (YAML). Validate before you trust it. |
| `cv-creation` | Run a per-application CV pipeline (match job → draft → export). |

**Private career data lives elsewhere.** This repo ships skills, docs, and fixtures only. Put real identity, evidence YAML, and applications in your own career tree.

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

Pick one path. Copy the paste-prompt into a new agent chat with this repo available.

| You want… | Open |
| :--- | :--- |
| Skills + reliable Python deps | [`prompts/install-full.md`](prompts/install-full.md) |
| Skills only; ask before any package install | [`prompts/install-lite.md`](prompts/install-lite.md) |

The agent should use **its own** skill-install location (see that product’s docs). Do not assume one vendor path.

---

## Web chat (no skills client)

**Normal web chat cannot install Agent Skills folders.** It cannot load `skills/evidence-bank` or `skills/cv-creation` from disk.

If you only have ChatGPT, Claude.ai, Gemini, or similar, use the weaker mega-prompt path: [`docs/web-chat.md`](docs/web-chat.md). Prefer Full or Lite when you can.

---

## Quick smoke (full path)

After Full install (or when PyYAML is already available):

```bash
python skills/evidence-bank/scripts/validate_evidence.py \
  skills/evidence-bank/assets/fixtures/ok.yaml
```

Expect a clean pass on the fixture. Real career YAML stays outside this repo.

---

## Builders / maintainers

Repo map (design, architecture, contract, agent load order): [`docs/README.md`](docs/README.md).

---

## License

MIT — see [`LICENSE`](LICENSE).
