# Solo-operator convenience targets for this skills pack.
# Prefer python3 (fallback: set PYTHON=python if needed).
# Run `make deps` once before `make smoke` / `make check` if PyYAML is missing.

PYTHON ?= python3
SKILL_ROOT ?= skills
MINI := $(SKILL_ROOT)/cv-creation/assets/fixtures/mini-app
APP := $(MINI)/applications/acme-de-2026-01-01
BAD := $(SKILL_ROOT)/cv-creation/assets/fixtures/grounding-bad

.PHONY: help deps deps-export test smoke-bank smoke-app smoke-grounding-bad smoke check

.DEFAULT_GOAL := help

help: ## List targets
	@echo "Targets (PYTHON=$(PYTHON); run make deps first if import yaml fails):"
	@echo "  help                 List targets with one-line descriptions (default)"
	@echo "  deps                 pip install requirements.txt + requirements-dev.txt"
	@echo "  deps-export          Same as deps, plus requirements-export.txt"
	@echo "  test                 pytest -q"
	@echo "  smoke-bank           validate_evidence OK fixture; bad fixture must fail"
	@echo "  smoke-app            validate_application (G4) + export_resume md,html"
	@echo "  smoke-grounding-bad  empty-ev-ids must fail validate_application"
	@echo "  smoke                smoke-bank + smoke-app + smoke-grounding-bad"
	@echo "  check                test + smoke"

deps: ## Install runtime + dev Python deps
	pip install -r requirements.txt -r requirements-dev.txt

deps-export: ## Install runtime + dev + export (docx/pdf) deps
	pip install -r requirements.txt -r requirements-dev.txt -r requirements-export.txt

test: ## Run pytest quietly
	pytest -q

smoke-bank: ## Evidence fixtures: OK pass, bad-missing-source must fail
	@echo "== smoke-bank: ok.yaml (expect exit 0) =="
	$(PYTHON) $(SKILL_ROOT)/evidence-bank/scripts/validate_evidence.py \
	  $(SKILL_ROOT)/evidence-bank/assets/fixtures/ok.yaml
	@echo "== smoke-bank: bad-missing-source.yaml (expect non-zero) =="
	@if $(PYTHON) $(SKILL_ROOT)/evidence-bank/scripts/validate_evidence.py \
	  $(SKILL_ROOT)/evidence-bank/assets/fixtures/bad-missing-source.yaml; then \
	  echo "expected validate_evidence to fail on bad-missing-source.yaml" >&2; \
	  exit 1; \
	fi
	@echo "smoke-bank OK"

smoke-app: ## Mini-app full G4 validate + md/html export (temp copy; fixtures stay clean)
	@echo "== smoke-app: validate_application (full G4 argv) =="
	$(PYTHON) $(SKILL_ROOT)/cv-creation/scripts/validate_application.py \
	  --style $(MINI)/profile/export-style.yaml \
	  --skills $(MINI)/profile/skills.yaml \
	  --composition $(APP)/composition.yaml \
	  --draft $(APP)/draft.md \
	  --evidence $(MINI)/profile/evidence.yaml \
	  --matching $(APP)/matching.yaml \
	  --identity $(MINI)/profile/identity.yaml
	@echo "== smoke-app: export_resume --formats md,html (temp copy) =="
	@tmp=$$(mktemp -d) && \
	  cp -a $(MINI)/. "$$tmp/" && \
	  $(PYTHON) $(SKILL_ROOT)/cv-creation/scripts/export_resume.py \
	    --formats md,html \
	    --career-root "$$tmp" \
	    "$$tmp/applications/acme-de-2026-01-01" && \
	  rm -rf "$$tmp"
	@echo "smoke-app OK"

smoke-grounding-bad: ## G4 empty-ev-ids must fail (like CI)
	@echo "== smoke-grounding-bad: empty-ev-ids (expect non-zero) =="
	@if $(PYTHON) $(SKILL_ROOT)/cv-creation/scripts/validate_application.py \
	  --style $(MINI)/profile/export-style.yaml \
	  --skills $(MINI)/profile/skills.yaml \
	  --composition $(BAD)/empty-ev-ids/composition.yaml \
	  --draft $(APP)/draft.md \
	  --evidence $(MINI)/profile/evidence.yaml \
	  --matching $(APP)/matching.yaml \
	  --identity $(MINI)/profile/identity.yaml; then \
	  echo "expected validate_application to fail on grounding-bad/empty-ev-ids" >&2; \
	  exit 1; \
	fi
	@echo "smoke-grounding-bad OK"

smoke: ## Architecture smoke (PyYAML must already be installed — make deps first)
	@$(MAKE) smoke-bank
	@$(MAKE) smoke-app
	@$(MAKE) smoke-grounding-bad
	@echo "smoke OK"

check: ## test + smoke
	@$(MAKE) test
	@$(MAKE) smoke
	@echo "check OK"
