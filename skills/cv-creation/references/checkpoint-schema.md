# Checkpoint schema

Path: `_skill_state/<app-id>/<timestamp>-<slug>.yaml`

Triggers: state transition; before lossy ops; every `turn_floor` (default 10); open flags ≥ `flag_threshold` (default 5); explicit command.

Retention: per app, keep `retention_k` (20) unpinned; pinned never deleted. Auto-pin checkpoint before a decision that is later revised.

```yaml
state:
  stage: matching
  items: { total: 14, done: 11, awaiting_hitl: 2, pending: 1 }
  revision_counts: {}
  open_flags: []
decisions: []
rejected: []
recent_context: []
```
