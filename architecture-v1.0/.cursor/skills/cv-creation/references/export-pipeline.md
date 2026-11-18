# Export pipeline

## Inputs

`draft.md`, `profile/identity.yaml`, `profile/export-style.yaml`. Never read `composition.yaml` or `export/` as inputs to the pipeline.

## Parse (stdlib regex)

Strip optional YAML frontmatter. Split on `^##\s+`. Within section: `^###\s+` subsection, `^[-*]\s+` bullet, blank-line prose. Lines before first `##` = header block.

Zero `##` sections → exit 2.

## Section model

header `{name, contact_lines}` + sections of blocks: paragraph | bullets | subsection`{heading, meta{org,dates}, bullets}`.

Identity wins on header mismatch (warn). Contact lines always from identity.

## Style MUST (exit 3 if violated)

`single_column: true`, `tables: false`, `text_boxes: false`, `content_headers_footers: false`, `real_list_styles: true`.

## Formats

md + html always (stdlib). docx if python-docx. pdf if weasyprint (HTML→PDF). Browser print of HTML is a user path, not automated.

## CLI

`export_resume.py [--formats md,html,docx,pdf] [--check-env] <app-dir>`

Exits: 0 ok/skip-optional; 1 missing requested dep; 2 parse; 3 style; 4 identity; 5 IO.
