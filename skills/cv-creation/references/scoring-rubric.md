# Scoring rubric

## Inputs

`requirements.yaml`, `requirement_skills`, `keywords.yaml` / `keyword_skills`.

## Formulas

```
contribution(skill, req) = importance_in_req × requirement_weight
priority_raw(skill)      = Σ over requirements
priority_norm            = 100 × priority_raw / max_raw
```

`requirement_weight`: must_have=1.5, strong=1.25, required=1.0, nice_to_have=0.75.

## ats_weight (1–5, tiebreaker only)

Local JD-keyword signal for scoring ties only — **not** an employer ATS rank or pass probability.

```
base = min(5, occurrences)
+2 if placement == title
+1 if placement == summary
+1 if raw matches ats_forms exactly
→ clamp to 1..5
```

Boilerplate-only keywords: mark `noise_candidate`, cap `ats_weight` at 1.

## Noise

`type: modifier` skills extracted but excluded from scoring; flag at G2.

## Output

Materialize `scores.yaml` (`job_skill_scores`). Always rebuild; never migrate.
