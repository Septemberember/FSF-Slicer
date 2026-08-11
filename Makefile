.PHONY: generate validate

generate:
	python3 scripts/generate_synthetic_preview.py

validate:
	python3 scripts/validate_preview.py

