from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import FSFValidationError
from .java_frontend import parse_java
from .models import FSFSpec
from .report import issues_to_dict, scenario_to_dict, slice_to_dict, write_reports
from .slicer import FSFGuidedSlicer, compile_slice
from .tbfv import TBFVEngine
from .validation import reconcile_spec, validate_fsf


def analyze(java_path: str | Path, fsf_path: str | Path, output_dir: str | Path, force: bool = False) -> dict[str, Any]:
    spec = FSFSpec.load(fsf_path)
    program = parse_java(java_path, spec.method)
    reconcile_spec(program, spec)
    validation = validate_fsf(program, spec)
    if not validation.valid and not force:
        messages = "; ".join(issue.message for issue in validation.issues if issue.severity == "error")
        raise FSFValidationError(f"FSF validation failed: {messages}")

    root = Path(output_dir)
    slices_dir = root / "slices"
    slicer = FSFGuidedSlicer(program, spec)
    original_engine = TBFVEngine(program, spec) if spec.config.compare_original else None
    slices: dict[str, Any] = {}
    sliced_results: dict[str, Any] = {}
    original_results: dict[str, Any] = {}

    for scenario in spec.scenarios:
        slice_result = slicer.slice(scenario, slices_dir)
        if spec.config.compile_slices:
            compile_slice(slice_result)
        slices[scenario.id] = slice_to_dict(slice_result)
        sliced_program = parse_java(slice_result.output_path, spec.method) if slice_result.output_path else program
        sliced_results[scenario.id] = scenario_to_dict(TBFVEngine(sliced_program, spec).verify(scenario))
        if original_engine:
            original_results[scenario.id] = scenario_to_dict(original_engine.verify(scenario))

    payload = {
        "tool": "FSF-Slicer-TBFV",
        "version": "1.0.0",
        "program": str(Path(java_path).resolve()),
        "fsf": str(Path(fsf_path).resolve()),
        "method": program.method_name,
        "analysis_domain": {name: {"type": value.type, "min": value.minimum, "max": value.maximum} for name, value in spec.inputs.items()},
        "limits": {
            "max_paths": spec.config.max_paths,
            "max_loop_iterations": spec.config.max_loop_iterations,
            "solver_timeout_ms": spec.config.solver_timeout_ms,
        },
        "validation": issues_to_dict(validation.issues),
        "slices": slices,
        "sliced_results": sliced_results,
        "original_results": original_results,
    }
    json_path, html_path = write_reports(payload, root)
    payload["report_json"] = str(json_path)
    payload["report_html"] = str(html_path)
    return payload


def slice_only(java_path: str | Path, fsf_path: str | Path, output_dir: str | Path) -> list[dict[str, Any]]:
    spec = FSFSpec.load(fsf_path)
    program = parse_java(java_path, spec.method)
    reconcile_spec(program, spec)
    report = validate_fsf(program, spec)
    if not report.valid:
        raise FSFValidationError("FSF validation failed; run validate-fsf for details.")
    slicer = FSFGuidedSlicer(program, spec)
    results = []
    for scenario in spec.scenarios:
        result = slicer.slice(scenario, output_dir)
        if spec.config.compile_slices:
            compile_slice(result)
        results.append(slice_to_dict(result))
    return results

