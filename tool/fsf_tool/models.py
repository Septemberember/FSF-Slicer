from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .errors import FSFValidationError


SUPPORTED_TYPES = {"byte", "short", "int", "long", "char", "boolean", "bool", "float", "double"}


@dataclass(slots=True)
class VariableSpec:
    name: str
    type: str
    minimum: int | float | None = None
    maximum: int | float | None = None
    source: str | None = None

    @classmethod
    def from_value(cls, name: str, value: str | dict[str, Any]) -> "VariableSpec":
        if isinstance(value, str):
            return cls(name=name, type=value)
        if not isinstance(value, dict) or "type" not in value:
            raise FSFValidationError(f"Variable '{name}' must be a type string or a mapping with 'type'.")
        return cls(
            name=name,
            type=str(value["type"]),
            minimum=value.get("min"),
            maximum=value.get("max"),
            source=value.get("source"),
        )


@dataclass(slots=True)
class FunctionalScenario:
    id: str
    testing_condition: str
    defining_condition: str
    description: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any], index: int) -> "FunctionalScenario":
        t = raw.get("T", raw.get("testing_condition"))
        d = raw.get("D", raw.get("defining_condition"))
        if not isinstance(t, str) or not isinstance(d, str):
            raise FSFValidationError(f"Scenario {index} requires string fields T and D.")
        return cls(str(raw.get("id", f"T{index}")), t.strip(), d.strip(), str(raw.get("description", "")))


@dataclass(slots=True)
class AnalysisConfig:
    max_paths: int = 128
    max_loop_iterations: int = 128
    solver_timeout_ms: int = 10_000
    default_int_min: int = -100
    default_int_max: int = 100
    compare_original: bool = True
    compile_slices: bool = True

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> "AnalysisConfig":
        raw = raw or {}
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in raw.items() if k in valid})


@dataclass(slots=True)
class FSFSpec:
    method: str | None
    inputs: dict[str, VariableSpec]
    outputs: dict[str, VariableSpec]
    scenarios: list[FunctionalScenario]
    config: AnalysisConfig = field(default_factory=AnalysisConfig)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "FSFSpec":
        source = Path(path)
        try:
            raw = yaml.safe_load(source.read_text(encoding="utf-8"))
        except Exception as exc:
            raise FSFValidationError(f"Cannot read FSF file {source}: {exc}") from exc
        if not isinstance(raw, dict):
            raise FSFValidationError("FSF root must be a YAML mapping.")
        inputs = {str(k): VariableSpec.from_value(str(k), v) for k, v in (raw.get("inputs") or {}).items()}
        output_raw = raw.get("outputs", raw.get("output", {}))
        if isinstance(output_raw, str):
            output_raw = {"return_value": output_raw}
        if isinstance(output_raw, dict) and "name" in output_raw and "type" in output_raw:
            output_raw = {str(output_raw["name"]): output_raw}
        outputs = {str(k): VariableSpec.from_value(str(k), v) for k, v in (output_raw or {}).items()}
        scenarios_raw = raw.get("scenarios") or []
        scenarios = [FunctionalScenario.from_dict(item, i + 1) for i, item in enumerate(scenarios_raw)]
        if not scenarios:
            raise FSFValidationError("FSF must contain at least one scenario.")
        return cls(
            method=raw.get("method"),
            inputs=inputs,
            outputs=outputs,
            scenarios=scenarios,
            config=AnalysisConfig.from_dict(raw.get("analysis")),
            metadata=raw.get("metadata") or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "inputs": {k: _variable_dict(v) for k, v in self.inputs.items()},
            "outputs": {k: _variable_dict(v) for k, v in self.outputs.items()},
            "scenarios": [
                {"id": s.id, "T": s.testing_condition, "D": s.defining_condition, "description": s.description}
                for s in self.scenarios
            ],
            "analysis": asdict(self.config),
            "metadata": self.metadata,
        }


def _variable_dict(value: VariableSpec) -> dict[str, Any]:
    result: dict[str, Any] = {"type": value.type}
    if value.minimum is not None:
        result["min"] = value.minimum
    if value.maximum is not None:
        result["max"] = value.maximum
    if value.source is not None:
        result["source"] = value.source
    return result


@dataclass(slots=True)
class ValidationIssue:
    severity: str
    code: str
    message: str
    counterexample: dict[str, Any] | None = None


@dataclass(slots=True)
class PathRecord:
    index: int
    test_case: dict[str, Any]
    path_condition: Any
    path_condition_text: str
    outputs: dict[str, Any]
    output_text: dict[str, str]
    trace: list[str]
    loop_iterations: int
    truncated: bool = False
    exception: str | None = None


@dataclass(slots=True)
class Judgment:
    status: str
    reason: str
    counterexample: dict[str, Any] | None = None


@dataclass(slots=True)
class ScenarioResult:
    scenario_id: str
    soundness: Judgment
    completeness: Judgment
    coverage: str
    paths: list[PathRecord]
    warnings: list[str] = field(default_factory=list)
    elapsed_ms: float = 0.0
