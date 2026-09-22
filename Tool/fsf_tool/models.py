from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import math
import re

import yaml

from .errors import FSFValidationError


SUPPORTED_TYPES = {"byte", "short", "int", "long", "char", "boolean", "bool", "float", "double"}
TYPE_LIMITS = {"byte": (-128, 127), "short": (-32768, 32767), "char": (0, 65535),
               "int": (-(2**31), 2**31-1), "long": (-(2**63), 2**63-1)}


class _UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise FSFValidationError(f"Duplicate or non-string YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _fields(raw, allowed, label):
    if not isinstance(raw, dict):
        raise FSFValidationError(f"{label} must be a mapping.")
    unknown = set(raw) - set(allowed)
    if unknown:
        raise FSFValidationError(f"Unknown {label} fields: {', '.join(sorted(unknown))}")


@dataclass(slots=True)
class VariableSpec:
    name: str
    type: str
    minimum: int | float | None = None
    maximum: int | float | None = None
    source: str | None = None

    def __post_init__(self):
        if not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", self.name):
            raise FSFValidationError(f"Invalid variable name: {self.name!r}")
        if self.type not in SUPPORTED_TYPES:
            raise FSFValidationError(f"Unsupported variable type: {self.type}")
        for value in (self.minimum, self.maximum):
            if value is None:
                continue
            if type(value) not in (int, float) or not math.isfinite(value):
                raise FSFValidationError(f"Bounds for {self.name} must be finite numbers.")
            if self.type in TYPE_LIMITS and (type(value) is not int or not TYPE_LIMITS[self.type][0] <= value <= TYPE_LIMITS[self.type][1]):
                raise FSFValidationError(f"Bound for {self.name} is outside the Java {self.type} range.")
            if self.type in {"bool", "boolean"}:
                raise FSFValidationError(f"Boolean variable {self.name} cannot have numeric bounds.")
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise FSFValidationError(f"Minimum exceeds maximum for {self.name}.")
        if self.source is not None and not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", self.source):
            raise FSFValidationError(f"Invalid output source for {self.name}.")

    @classmethod
    def from_value(cls, name: str, value: str | dict[str, Any]) -> "VariableSpec":
        if isinstance(value, str):
            return cls(name=name, type=value)
        if not isinstance(value, dict) or "type" not in value:
            raise FSFValidationError(f"Variable '{name}' must be a type string or a mapping with 'type'.")
        _fields(value, {"type", "min", "max", "source", "name"}, f"variable {name}")
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

    def __post_init__(self):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", self.id):
            raise FSFValidationError("Scenario IDs must be portable names of 1-80 letters, digits, '_' or '-'.")
        if self.id.split('.')[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}:
            raise FSFValidationError(f"Reserved scenario ID: {self.id}")
        if not self.testing_condition or not self.defining_condition:
            raise FSFValidationError(f"Scenario {self.id} requires nonempty T and D.")

    @classmethod
    def from_dict(cls, raw: dict[str, Any], index: int) -> "FunctionalScenario":
        _fields(raw, {"id", "T", "D", "testing_condition", "defining_condition", "description"}, "scenario")
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
    random_seed: int = 0
    check_preservation: bool = True
    slicing_mode: str = "fsf"

    def __post_init__(self):
        for name in ("max_paths", "max_loop_iterations", "solver_timeout_ms"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise FSFValidationError(f"{name} must be a positive integer.")
        for name in ("compare_original", "compile_slices", "check_preservation"):
            if type(getattr(self, name)) is not bool:
                raise FSFValidationError(f"{name} must be a Boolean.")
        if type(self.random_seed) is not int or not 0 <= self.random_seed < 2**31:
            raise FSFValidationError("random_seed must be an integer in [0, 2^31).")
        if any(type(v) is not int for v in (self.default_int_min, self.default_int_max)) or not -(2**31) <= self.default_int_min <= self.default_int_max < 2**31:
            raise FSFValidationError("Default integer bounds must be ordered Java int values.")
        if self.slicing_mode not in {"fsf", "backward", "conditioned"}:
            raise FSFValidationError("slicing_mode must be fsf, backward, or conditioned.")

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> "AnalysisConfig":
        raw = {} if raw is None else raw
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        _fields(raw, valid, "analysis")
        return cls(**raw)


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
            raw = yaml.load(source.read_text(encoding="utf-8"), Loader=_UniqueLoader)
        except Exception as exc:
            raise FSFValidationError(f"Cannot read FSF file {source}: {exc}") from exc
        if not isinstance(raw, dict):
            raise FSFValidationError("FSF root must be a YAML mapping.")
        _fields(raw, {"method", "inputs", "outputs", "output", "scenarios", "analysis", "metadata"}, "FSF")
        if raw.get("method") is not None and not isinstance(raw["method"], str):
            raise FSFValidationError("method must be a string.")
        if not isinstance(raw.get("inputs", {}), dict) or not isinstance(raw.get("metadata", {}), dict):
            raise FSFValidationError("inputs and metadata must be mappings.")
        inputs = {str(k): VariableSpec.from_value(str(k), v) for k, v in raw.get("inputs", {}).items()}
        output_raw = raw.get("outputs", raw.get("output", {}))
        if isinstance(output_raw, str):
            output_raw = {"return_value": output_raw}
        if isinstance(output_raw, dict) and "name" in output_raw and "type" in output_raw:
            output_raw = {str(output_raw["name"]): output_raw}
        if not isinstance(output_raw, dict):
            raise FSFValidationError("outputs must be a mapping.")
        outputs = {str(k): VariableSpec.from_value(str(k), v) for k, v in output_raw.items()}
        if set(inputs) & set(outputs):
            raise FSFValidationError("Input and output names must be distinct.")
        scenarios_raw = raw.get("scenarios") or []
        if not isinstance(scenarios_raw, list):
            raise FSFValidationError("scenarios must be a list.")
        scenarios = [FunctionalScenario.from_dict(item, i + 1) for i, item in enumerate(scenarios_raw)]
        if len({s.id.casefold() for s in scenarios}) != len(scenarios):
            raise FSFValidationError("Scenario IDs must be unique, ignoring case.")
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
