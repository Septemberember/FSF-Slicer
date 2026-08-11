from pathlib import Path

from fsf_tool.java_frontend import parse_java
from fsf_tool.models import FSFSpec
from fsf_tool.validation import reconcile_spec, validate_fsf


ROOT = Path(__file__).resolve().parents[1]


def test_calculator_fsf_is_formally_well_formed():
    spec = FSFSpec.load(ROOT / "examples/calculator.fsf.yaml")
    program = parse_java(ROOT / "examples/Calculator.java", spec.method)
    reconcile_spec(program, spec)
    report = validate_fsf(program, spec)
    assert not [item for item in report.issues if item.severity == "error"]

