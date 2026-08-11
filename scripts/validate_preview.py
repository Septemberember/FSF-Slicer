#!/usr/bin/env python3
"""Validate the structure and aggregates of the synthetic artifact preview."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = ROOT / "data" / "synthetic"
REPORTED_DIR = ROOT / "data" / "paper-reported"
STATUS = "SYNTHETIC_ILLUSTRATIVE"

EXPECTED = {
    "Branched": {
        "programs": 100,
        "tasks": 339,
        "rq1": ("0.4690", "0.3546", "0.3478"),
        "rq2": ("0.653", "0.721", "0.660", "0.682"),
        "definite": 333,
        "inconclusive": 6,
    },
    "Sequential": {
        "programs": 63,
        "tasks": 137,
        "rq1": ("0.9930", "1.0000", "1.0000"),
        "rq2": ("0.943", "0.982", "0.964", "0.971"),
        "definite": 133,
        "inconclusive": 4,
    },
    "Single-path-Loop": {
        "programs": 21,
        "tasks": 57,
        "rq1": ("0.7340", "0.5998", "0.7000"),
        "rq2": ("0.893", "0.849", "0.863", "0.874"),
        "definite": 53,
        "inconclusive": 4,
    },
    "Multi-path-Loop": {
        "programs": 31,
        "tasks": 104,
        "rq1": ("0.5780", "0.5000", "0.5553"),
        "rq2": ("0.742", "0.750", "0.745", "0.746"),
        "definite": 104,
        "inconclusive": 0,
    },
    "Nested-Loop": {
        "programs": 35,
        "tasks": 103,
        "rq1": ("0.5130", "0.4875", "0.4702"),
        "rq2": ("0.865", "0.806", "0.702", "0.794"),
        "definite": 95,
        "inconclusive": 8,
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rounded(value: Decimal, places: int) -> Decimal:
    quantum = Decimal("1").scaleb(-places)
    return value.quantize(quantum, rounding=ROUND_HALF_UP)


def mean(values: list[Decimal]) -> Decimal:
    return sum(values, Decimal("0")) / Decimal(len(values))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_status(rows: list[dict[str, str]], name: str) -> None:
    require(rows, f"{name} is empty")
    require(all(row.get("data_status") == STATUS for row in rows), f"{name} contains an unmarked row")


def validate_manifests() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    programs = read_csv(SYNTHETIC_DIR / "program_manifest.csv")
    tasks = read_csv(SYNTHETIC_DIR / "task_manifest.csv")
    validate_status(programs, "program_manifest.csv")
    validate_status(tasks, "task_manifest.csv")
    require(len(programs) == 250, f"Expected 250 programs, found {len(programs)}")
    require(len(tasks) == 740, f"Expected 740 tasks, found {len(tasks)}")
    program_ids = {row["program_id"] for row in programs}
    task_ids = {row["task_id"] for row in tasks}
    require(len(program_ids) == len(programs), "Duplicate program identifier")
    require(len(task_ids) == len(tasks), "Duplicate task identifier")
    require(all(row["program_id"] in program_ids for row in tasks), "Task references an unknown program")
    program_counts = Counter(row["category"] for row in programs)
    task_counts = Counter(row["category"] for row in tasks)
    scenarios_by_program = Counter(row["program_id"] for row in tasks)
    for category, expected in EXPECTED.items():
        require(program_counts[category] == expected["programs"], f"Program count mismatch for {category}")
        require(task_counts[category] == expected["tasks"], f"Task count mismatch for {category}")
    for row in programs:
        require(
            int(row["scenario_count"]) == scenarios_by_program[row["program_id"]],
            f"Scenario count mismatch for {row['program_id']}",
        )
    return programs, tasks


def validate_rq1(task_ids: set[str]) -> None:
    rows = read_csv(SYNTHETIC_DIR / "rq1_scale.csv")
    validate_status(rows, "rq1_scale.csv")
    require(len(rows) == 740, f"Expected 740 RQ1 rows, found {len(rows)}")
    require({row["task_id"] for row in rows} == task_ids, "RQ1 task set differs from manifest")
    ratio_fields = (
        ("original_loc", "slice_loc", "loc_ratio"),
        (
            "original_executable_statements",
            "slice_executable_statements",
            "executable_statement_ratio",
        ),
        (
            "original_cyclomatic_complexity",
            "slice_cyclomatic_complexity",
            "cyclomatic_complexity_ratio",
        ),
    )
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    originals_by_program: dict[str, set[tuple[str, str, str]]] = defaultdict(set)
    for row in rows:
        grouped[row["category"]].append(row)
        originals_by_program[row["program_id"]].add(
            (
                row["original_loc"],
                row["original_executable_statements"],
                row["original_cyclomatic_complexity"],
            )
        )
        for original_field, slice_field, ratio_field in ratio_fields:
            original = Decimal(row[original_field])
            sliced = Decimal(row[slice_field])
            stated = Decimal(row[ratio_field])
            require(Decimal("0") < sliced <= original, f"Invalid RQ1 metric for {row['task_id']}")
            require(abs(stated - sliced / original) <= Decimal("0.0000005"), f"RQ1 ratio mismatch for {row['task_id']}")
    require(all(len(values) == 1 for values in originals_by_program.values()), "Original metrics vary across a program's tasks")
    for category, expected in EXPECTED.items():
        category_rows = grouped[category]
        for metric_index, (_, _, ratio_field) in enumerate(ratio_fields):
            actual = rounded(mean([Decimal(row[ratio_field]) for row in category_rows]), 4)
            require(actual == Decimal(expected["rq1"][metric_index]), f"RQ1 aggregate mismatch for {category}/{ratio_field}: {actual}")
    for metric_index, (_, _, ratio_field) in enumerate(ratio_fields):
        actual = rounded(mean([Decimal(row[ratio_field]) for row in rows]), 4)
        expected_overall = (Decimal("0.6079"), Decimal("0.5319"), Decimal("0.5419"))[metric_index]
        require(actual == expected_overall, f"RQ1 overall mismatch for {ratio_field}: {actual}")


def validate_rq2(task_ids: set[str]) -> None:
    rows = read_csv(SYNTHETIC_DIR / "rq2_timing_runs.csv")
    validate_status(rows, "rq2_timing_runs.csv")
    require(len(rows) == 7400, f"Expected 7,400 RQ2 rows, found {len(rows)}")
    by_task: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        require(row["task_id"] in task_ids, f"Unknown RQ2 task {row['task_id']}")
        by_task[row["task_id"]].append(row)
        phase_pairs = (
            ("original_dynamic_ms", "slice_dynamic_ms", "dynamic_ratio"),
            ("original_path_derivation_ms", "slice_path_derivation_ms", "path_derivation_ratio"),
            ("original_smt_ms", "slice_smt_ms", "smt_ratio"),
            ("original_total_ms", "slice_total_ms", "total_ratio"),
        )
        for original_field, slice_field, ratio_field in phase_pairs:
            original = Decimal(row[original_field])
            sliced = Decimal(row[slice_field])
            stated = Decimal(row[ratio_field])
            require(original > 0 and sliced > 0, f"Non-positive RQ2 duration for {row['task_id']}")
            require(abs(stated - sliced / original) <= Decimal("0.000001"), f"RQ2 ratio mismatch for {row['task_id']}")
        original_sum = (
            Decimal(row["original_dynamic_ms"])
            + Decimal(row["original_path_derivation_ms"])
            + Decimal(row["original_smt_ms"])
            + Decimal(row["original_other_ms"])
        )
        slice_sum = (
            Decimal(row["slice_dynamic_ms"])
            + Decimal(row["slice_path_derivation_ms"])
            + Decimal(row["slice_smt_ms"])
            + Decimal(row["slice_slicing_ms"])
            + Decimal(row["slice_other_ms"])
        )
        require(abs(original_sum - Decimal(row["original_total_ms"])) <= Decimal("0.000003"), "Original total does not sum")
        require(abs(slice_sum - Decimal(row["slice_total_ms"])) <= Decimal("0.000004"), "Slice total does not sum")
    require(set(by_task) == task_ids, "RQ2 task set differs from manifest")
    for task_id, task_rows in by_task.items():
        require(len(task_rows) == 10, f"Expected ten repetitions for {task_id}")
        require({int(row["repetition"]) for row in task_rows} == set(range(1, 11)), f"Invalid repetition set for {task_id}")

    task_ratios: dict[str, dict[str, Decimal]] = {}
    for task_id, task_rows in by_task.items():
        task_ratios[task_id] = {
            field: mean([Decimal(row[field]) for row in task_rows])
            for field in ("dynamic_ratio", "path_derivation_ratio", "smt_ratio", "total_ratio")
        }
    category_by_task = {task_id: task_rows[0]["category"] for task_id, task_rows in by_task.items()}
    fields = ("dynamic_ratio", "path_derivation_ratio", "smt_ratio", "total_ratio")
    for category, expected in EXPECTED.items():
        category_task_ids = [task_id for task_id, value in category_by_task.items() if value == category]
        for metric_index, field in enumerate(fields):
            actual = rounded(mean([task_ratios[task_id][field] for task_id in category_task_ids]), 3)
            require(actual == Decimal(expected["rq2"][metric_index]), f"RQ2 aggregate mismatch for {category}/{field}: {actual}")
    for metric_index, field in enumerate(fields):
        actual = rounded(mean([values[field] for values in task_ratios.values()]), 3)
        expected_overall = (Decimal("0.767"), Decimal("0.795"), Decimal("0.750"), Decimal("0.775"))[metric_index]
        require(actual == expected_overall, f"RQ2 overall mismatch for {field}: {actual}")


def validate_rq3(task_ids: set[str]) -> None:
    rows = read_csv(SYNTHETIC_DIR / "rq3_preservation.csv")
    validate_status(rows, "rq3_preservation.csv")
    require(len(rows) == 740, f"Expected 740 RQ3 rows, found {len(rows)}")
    require({row["task_id"] for row in rows} == task_ids, "RQ3 task set differs from manifest")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)
        require(row["original_availability"] == row["slice_availability"], f"Mixed availability for {row['task_id']}")
        if row["original_availability"] == "DEFINITE":
            require(row["original_soundness"] == row["slice_soundness"], f"Soundness mismatch for {row['task_id']}")
            require(row["original_completeness"] == row["slice_completeness"], f"Completeness mismatch for {row['task_id']}")
            require(row["soundness_agreement"] == "TRUE", f"Missing soundness agreement for {row['task_id']}")
            require(row["completeness_agreement"] == "TRUE", f"Missing completeness agreement for {row['task_id']}")
            require(not row["inconclusive_reason"], f"Unexpected reason for definite task {row['task_id']}")
        else:
            require(bool(row["inconclusive_reason"]), f"Missing reason for inconclusive task {row['task_id']}")
    total_definite = 0
    total_inconclusive = 0
    for category, expected in EXPECTED.items():
        category_rows = grouped[category]
        definite = sum(row["original_availability"] == "DEFINITE" for row in category_rows)
        inconclusive = len(category_rows) - definite
        require(definite == expected["definite"], f"RQ3 definite count mismatch for {category}")
        require(inconclusive == expected["inconclusive"], f"RQ3 inconclusive count mismatch for {category}")
        total_definite += definite
        total_inconclusive += inconclusive
    require(total_definite == 718 and total_inconclusive == 22, "RQ3 overall availability mismatch")
    require(rounded(Decimal(total_definite) / Decimal(740) * 100, 2) == Decimal("97.03"), "RQ3 conclusive rate mismatch")


def validate_reported_summaries() -> None:
    for filename, table in (
        ("rq1_category_summary.csv", "MANUSCRIPT_TABLE_2"),
        ("rq2_category_summary.csv", "MANUSCRIPT_TABLE_3"),
        ("rq3_category_summary.csv", "MANUSCRIPT_TABLE_4"),
    ):
        rows = read_csv(REPORTED_DIR / filename)
        require(len(rows) == 6, f"Expected five categories and overall in {filename}")
        require(all(row["source"] == table for row in rows), f"Invalid source label in {filename}")


def validate_metadata() -> None:
    metadata = json.loads((SYNTHETIC_DIR / "metadata.json").read_text(encoding="utf-8"))
    require(metadata["data_status"] == STATUS, "Metadata status mismatch")
    require(metadata["empirical"] is False, "Synthetic metadata cannot claim empirical provenance")
    require(metadata["program_count"] == 250, "Metadata program count mismatch")
    require(metadata["task_count"] == 740, "Metadata task count mismatch")
    require(metadata["rq2_repetitions_per_task"] == 10, "Metadata repetition count mismatch")


def main() -> None:
    _, tasks = validate_manifests()
    task_ids = {row["task_id"] for row in tasks}
    validate_rq1(task_ids)
    validate_rq2(task_ids)
    validate_rq3(task_ids)
    validate_reported_summaries()
    validate_metadata()
    print("PASS: synthetic preview is structurally consistent.")
    print("PASS: 250 programs, 740 tasks, and 7,400 timing rows are present.")
    print("PASS: generated category and overall aggregates match manuscript Tables 2-4 after rounding.")
    print("PASS: every generated record is marked SYNTHETIC_ILLUSTRATIVE.")


if __name__ == "__main__":
    main()
