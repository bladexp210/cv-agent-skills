# Adversarial scripts pass (scoped red-team)

Paste-ready brief for the operator to run in **dsh** (or any client) with a **different AI model** than authored these scripts.

---

## Goal

Scoped security / integrity review of cold-path validators and export — find bypasses, injection, path abuse, and dishonest exits.

## Out of scope

- Full product audit, HITL UX review, career-data privacy policy rewrite
- Refactoring or “fixing” production scripts unless a finding is **Critical** and the operator confirms
- Network probing, exfiltration, or touching real career trees outside this checkout / `/tmp` copies

---

## Targets

**Primary (must deep-read + attempt PoCs):**

- `skills/cv-creation/scripts/export_resume.py`
- `skills/cv-creation/scripts/validate_application.py`

**Secondary (skim only):**

- `skills/evidence-bank/scripts/validate_evidence.py` — exit-code / parse abuse only (do not expand into a full bank audit)

---

## Hard rules

1. Do **not** edit production scripts in this pass unless the finding is **Critical** and the operator confirms in-session.
2. Prefer a written report + optional PoC fixtures under `/tmp` (temp copies of mini-app / grounding fixtures).
3. Never phone home; no network probes beyond reading code in the checkout.
4. Do not exfiltrate secrets, career PII, or env credentials.
5. Work from this repo checkout (and `/tmp` copies). Do not mutate `career-v3` or other private career projects.

---

## Attack surface checklist (must cover)

1. **PDF `deny_external_url_fetcher`** — `http` / `https` / `file` / protocol-relative / `data:` edge cases; confirm every WeasyPrint path always passes the deny fetcher.
2. **`page.size` / margin injection** into CSS (allowlist / pattern bypasses).
3. **HTML / docx escaping** of identity and draft fields (XSS-shaped or XML-break values).
4. **Path traversal** via `--career-root`, `app_dir`, or style paths — writes must stay under `export/` only.
5. **G4 grounding bypasses** — empty ids, draft mismatch, non-fact, uncovered, skill not on evidence, cited-not-listed: confirm validator fails; try **novel** bypasses not already in fixtures.
6. **Exit code honesty** vs [`SECURITY.md`](../SECURITY.md) matrix (wrong exit = finding).
7. **Unexpected errors** — unreadable YAML, missing keys, huge inputs: fail closed vs crash with unclear exit.
8. **Import / side effects at module load** (network, writes, surprising I/O on import).

---

## Method

1. Read [`SECURITY.md`](../SECURITY.md), the target scripts, and existing tests under `tests/` first.
2. Attempt PoCs with **temp copies** of `skills/cv-creation/assets/fixtures/mini-app` (and grounding-bad as needed).
3. If the environment allows: `make test` / `pytest -q` (and targeted smoke commands). Do not require PDF for this pass unless exercising the WeasyPrint path explicitly.

---

## Deliverable format (required)

### Summary verdict

One line: **Pass with notes** | **Issues found**

### Findings table

| id | severity | script | claim | repro steps | expected vs actual | suggested fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| … | Critical / High / Medium / Low | … | … | … | … | … |

### Checklist coverage

Explicit list of checklist items **attempted** vs **skipped** (with reason if skipped).

### What the operator should verify on the real surface

Concrete commands (from repo root), e.g. `make smoke`, specific `python3 …/export_resume.py` / `validate_application.py` invocations against `/tmp` PoCs — not chat-summary-only.

---

Paste this whole prompt into dsh with a model that did not author these scripts.
