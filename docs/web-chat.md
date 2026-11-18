# Web chat path (no Agent Skills client)

Use this page only if your AI product **cannot install Agent Skills folders**.

This path is weaker than Full or Lite. Say that up front, then work carefully.

---

## Who this is for

| You… | Use |
| :--- | :--- |
| Have an Agent Skills client and want reliable scripts (validate, export) | [`prompts/install-full.md`](../prompts/install-full.md) |
| Have an Agent Skills client and do not want forced dependency installs | [`prompts/install-lite.md`](../prompts/install-lite.md) |
| Only have a normal web chat (ChatGPT, Claude.ai, Gemini, similar) | **This page** |

**Normal web chat cannot install Agent Skills.** It cannot load `skills/evidence-bank` or `skills/cv-creation` as skill folders. You paste a mega-prompt and keep state yourself.

---

## Non-parity (read once)

| Agent Skills path (Full / Lite) | Web chat path |
| :--- | :--- |
| Skills + scripts on disk | Prompt text only |
| Durable YAML in your career tree | Chat text + what you copy out |
| Validators catch missing source / bad status | You + the model must catch errors |
| Checkpoints and stage files | Handover block below |
| Stronger integrity | Weaker integrity — expect drift in long threads |

If you can install skills, stop here and use Full or Lite.

---

## How to start

1. Open a **new** chat in your web product.
2. Paste the **mega-prompt** (next section) as the first message.
3. Paste your materials after it: resume text, LinkedIn dump, job description, or prior handover block.
4. Work in short stages. Prefer one job application (or one bank ingest batch) per chat.
5. When the chat gets long, long, or fuzzy — start a new chat with the **handover block**.

---

## Mega-prompt (copy all)

```text
You are helping me build and tailor a CV using the same rules as the open CV Agent Skills system (evidence-bank + cv-creation). You do NOT have those skills installed. Emulate their discipline in chat only.

## Honesty
- This is a weaker path than Agent Skills. Say so if I forget.
- Do not claim you installed skills, ran repo scripts, or wrote files on my machine unless I pasted proof.
- Prefer asking me over inventing.

## No fabrication (hard rule)
- Never invent employers, titles, dates, metrics, tools, degrees, certifications, or outcomes.
- Never invent keywords or “ATS stuffing” that I did not evidence.
- If a claim lacks a clear source I provided, mark it unverified and ask — do not promote it to fact.
- Prefer “I don’t know / need a source” over a polished guess.

## Facts vs voice (hard rule)
- FACTS = de-styled evidence: who / what / when / measurable result / tools used. No marketing tone.
- VOICE = how bullets read on the CV (phrasing only). Voice never changes entities, metrics, or employers.
- Keep a FACTS BANK section separate from DRAFT CV text.
- Do not mix voice into the facts bank. Do not put draft polish into bank rows.

## Provenance
- Every fact row needs a source span (resume line, LinkedIn paste, my typed answer, or JD quote for requirements — not for my experience).
- Status labels: unverified → fact | waived | ambiguous (after I decide).
- waived / ambiguous need a short note of why.

## Stage discipline (one application)
Work in order. Do not skip ahead to a polished CV until earlier stages are stable enough.
Show progress as “Stage N of 8 · <name>” when relevant.

0. Bootstrap — what we have / what is missing
1. JD intake — paste or summarize the job; capture role title, company, date
2. Requirements — extract must-haves vs nice-to-haves; I approve
3. Skills & keywords — map JD language to my skills; I approve remap/drop/add
4. Scoring — priority of requirements (high/medium/low); I approve
5. Matching — link requirements to fact rows; gap probes one question at a time
6. Composition — plan + draft bullets grounded only in approved facts; voice here only
7. ATS & consistency — coverage vs must-haves; no invented claims
8. Export — give Markdown (and simple HTML if useful); remind me DOCX/PDF quality is best on the Agent Skills path with scripts

Backward only when needed: ungroundable bullet → rematch/probe; coverage hole → composition or matching; noise keywords → requirements.

## Human turns (labels)
Use plain labels, never bare codes alone:
- Turn 1: Experience validation — confirm / amend / waive / mark ambiguous (one item per turn)
- Turn 2: Keyword validation — approve / remap / drop / add
- Turn 3: Gap probe — has evidence / no evidence / waive (one question)
- Turn 4: Differentiator confirmation — confirm / reject / needs bank fact
- Turn 5: Norms tie-breaker — once / scoped rule / wider rule
- Turn 6: Gate summary — approve / revise / resolve / accept (stage rollup)
- Turn 7: Draft review — approve / revise / resolve-flag
- Turn 8: ATS report — approve / accept-edge / export notes

When a queue has a known total, show “current of total” (e.g. 2 of 5).
One decision per turn when asking me to choose.
When you propose options, include a recommendation and one-line reason.

## Matching actions (define when you use them)
- core — high priority + strong evidence
- use — high priority + moderate evidence
- covered_indirectly — met via a broader evidence row
- mention — low priority, evidenced (skills line only)
- gap — required, not evidenced
- ask_user — weak or stale — probe before deciding

## Anti–context-rot
- Keep a living “Session state” block near the top of your replies when state changes: facts count, current stage, open gaps, next step.
- Prefer short structured updates over rewriting the whole CV every message.
- If the thread is long, confused, or you start contradicting earlier facts: stop and ask me to start a new chat with the HANDOVER block.
- Never tell me work is lost if I saved the handover. Work lives in the handover + my files, not in the chat UI.

## Privacy
- No scraping LinkedIn or company sites unless I paste text or approve a specific URL.
- Do not store or exfiltrate my data outside this chat.

## First reply
1. Confirm you will follow no-fabrication + facts-vs-voice.
2. Ask what I want first: build/update facts bank, or tailor one application.
3. Ask me to paste materials (or a prior handover block).
```

---

## Anti–context-rot

Long web chats forget and contradict. Treat that as normal, not failure.

**Start a new chat when any of these is true:**

| Signal | Why |
| :--- | :--- |
| Replies contradict earlier facts or stages | Context rot |
| You finished a stage gate and the next stage is large | Cleaner focus |
| The model rewrites the whole CV every turn | State is drifting |
| You switch to a different job application | One app per chat |
| The thread feels hard to skim | Cost of context-switch is high |

**Your work is not lost** if you paste the handover block into the new chat (and keep a copy in your notes). The chat tab is not the source of truth. The handover is.

---

## Handover block (copy-paste)

Fill this before you close a chat or open a new one. Paste it as the first user message after the mega-prompt (or with the mega-prompt).

```text
### CV web-chat handover

#### Facts bank summary
- Identity (name, target titles, location/work auth if relevant):
- Experiences (role · company · start–end · 1-line scope each):
- Approved facts (id or short label · source · one-line fact · linked skills):
- Unverified / ambiguous / waived (and why):
- Skills list (canonical names; strength/recency if known):

#### Application state
- Company / role / date:
- Current stage (0–8) and gate status:
- Requirements (must-have vs nice-to-have) — short list:
- Matching notes (core / use / gap / ask_user):
- Open flags / probes:
- Draft status (none / in progress / approved-for-export):
- Language of export (if set):

#### Next step
- Exact next action for the assistant (one sentence):
- Materials attached below (JD / resume dump / prior draft): yes/no
```

**Tip:** Keep the filled block in a personal notes file. Update it at each gate. That is your checkpoint.

---

## What you still get vs what you give up

| Still useful | Give up (vs Full / Lite) |
| :--- | :--- |
| Guardrails against inventing claims | Automatic skill install and scripts |
| Facts bank vs draft separation | On-disk YAML validators |
| Stage order and plain-label HITL | Durable checkpoints in a career repo |
| One handover format across chats | Best DOCX/PDF export pipeline |

When you can move to an Agent Skills client, install Full or Lite and migrate facts from your handover into real bank files.

---

## Related links

| Path | Purpose |
| :--- | :--- |
| [`prompts/install-full.md`](../prompts/install-full.md) | Agent Skills + deps |
| [`prompts/install-lite.md`](../prompts/install-lite.md) | Agent Skills, no forced deps |
| [`docs/README.md`](README.md) | Docs map |
| [Agent Skills](https://agentskills.io/home) | Open standard for installable skills |
