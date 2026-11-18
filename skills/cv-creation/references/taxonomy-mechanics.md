# Taxonomy mechanics

File: `profile/skills.yaml`.

Lookup: canonical_name, aliases, ats_forms (casefold). **New sk_*: HITL before write.** Merge: survivor keeps id; loser becomes alias; rewrite references. Modifiers excluded from scoring. Parents: DAG; validator rejects cycles/unknown parent_id. Soft delete: `deprecated: true`.
