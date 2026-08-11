#!/usr/bin/env python3
"""Generate deterministic, explicitly synthetic records for artifact review."""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = ROOT / "data" / "synthetic"
REPORTED_DIR = ROOT / "data" / "paper-reported"
SEED = 20260810
STATUS = "SYNTHETIC_ILLUSTRATIVE"

CATEGORIES = [
    {
        "category": "Branched",
        "prefix": "BR",
        "programs": 100,
        "tasks": 339,
        "rq1": (Decimal("0.4690"), Decimal("0.3546"), Decimal("0.3478")),
        "rq2": (Decimal("0.653"), Decimal("0.721"), Decimal("0.660"), Decimal("0.682")),
        "definite": 333,
        "inconclusive": 6,
    },
    {
        "category": "Sequential",
        "prefix": "SQ",
        "programs": 63,
        "tasks": 137,
        "rq1": (Decimal("0.9930"), Decimal("1.0000"), Decimal("1.0000")),
        "rq2": (Decimal("0.943"), Decimal("0.982"), Decimal("0.964"), Decimal("0.971")),
        "definite": 133,
        "inconclusive": 4,
    },
    {
        "category": "Single-path-Loop",
        "prefix": "SL",
        "programs": 21,
        "tasks": 57,
        "rq1": (Decimal("0.7340"), Decimal("0.5998"), Decimal("0.7000")),
        "rq2": (Decimal("0.893"), Decimal("0.849"), Decimal("0.863"), Decimal("0.874")),
        "definite": 53,
        "inconclusive": 4,
    },
    {
        "category": "Multi-path-Loop",
        "prefix": "ML",
        "programs": 31,
        "tasks": 104,
        "rq1": (Decimal("0.5780"), Decimal("0.5000"), Decimal("0.5553")),
        "rq2": (Decimal("0.742"), Decimal("0.750"), Decimal("0.745"), Decimal("0.746")),
        "definite": 104,
        "inconclusive": 0,
    },
    {
        "category": "Nested-Loop",
        "prefix": "NL",
        "programs": 35,
        "tasks": 103,
        "rq1": (Decimal("0.5130"), Decimal("0.4875"), Decimal("0.4702")),
        "rq2": (Decimal("0.865"), Decimal("0.806"), Decimal("0.702"), Decimal("0.794")),
        "definite": 95,
        "inconclusive": 8,
    },
]

RQ1_OVERALL = (Decimal("0.6079"), Decimal("0.5319"), Decimal("0.5419"))
RQ2_OVERALL = (Decimal("0.767"), Decimal("0.795"), Decimal("0.750"), Decimal("0.775"))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def scenario_count_distribution(programs: int, tasks: int) -> list[int]:
    base, remainder = divmod(tasks, programs)
    return [base + (1 if index < remainder else 0) for index in range(programs)]


def illustrative_scenario(category: str, scenario_index: int) -> tuple[str, str]:
    slot = scenario_index - 1
    if category == "Branched":
        return f"mode == {slot}", f"return_value == branch_value_{slot}"
    if category == "Sequential":
        return f"input >= {slot}", f"return_value == input + {slot}"
    if category == "Single-path-Loop":
        return f"limit >= {slot}", "return_value == accumulated_value"
    if category == "Multi-path-Loop":
        return f"limit >= {slot} && mode == {slot % 2}", "return_value == selected_accumulation"
    return f"outer_limit >= {slot} && inner_limit >= 0", "return_value == nested_accumulation"


def mean_ratio(rows: list[dict[str, object]], original_key: str, slice_key: str) -> Decimal:
    return sum(
        (Decimal(int(row[slice_key])) / Decimal(int(row[original_key])) for row in rows),
        Decimal("0"),
    ) / Decimal(len(rows))


def adjust_integer_ratios(
    rows: list[dict[str, object]], original_key: str, slice_key: str, target: Decimal
) -> None:
    """Adjust integer slice metrics until the category mean rounds to four decimals."""
    # Keep the unrounded category mean close enough to its displayed value that
    # the task-weighted overall mean is stable at the manuscript's precision.
    tolerance = Decimal("0.0000049")
    for _ in range(200000):
        current = mean_ratio(rows, original_key, slice_key)
        if abs(current - target) <= tolerance:
            return
        direction = 1 if current < target else -1
        best_row = None
        best_error = abs(current - target)
        for row in rows:
            original = int(row[original_key])
            sliced = int(row[slice_key])
            candidate = sliced + direction
            if candidate < 1 or candidate > original:
                continue
            candidate_mean = current + Decimal(direction) / Decimal(original * len(rows))
            error = abs(candidate_mean - target)
            if error < best_error:
                best_error = error
                best_row = row
        if best_row is None:
            raise RuntimeError(f"Could not tune {slice_key} to {target}")
        best_row[slice_key] = int(best_row[slice_key]) + direction
    raise RuntimeError(f"Adjustment limit exceeded for {slice_key}")


def centered_ratios(target: Decimal, count: int, salt: int) -> list[Decimal]:
    raw_offsets = [Decimal(((index * 17 + salt * 13) % 21) - 10) / Decimal("1000") for index in range(count)]
    mean_offset = sum(raw_offsets, Decimal("0")) / Decimal(count)
    return [target + offset - mean_offset for offset in raw_offsets]


def generate() -> None:
    rng = random.Random(SEED)
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    REPORTED_DIR.mkdir(parents=True, exist_ok=True)

    program_rows: list[dict[str, object]] = []
    task_rows: list[dict[str, object]] = []
    rq1_rows: list[dict[str, object]] = []
    tasks_by_category: dict[str, list[dict[str, object]]] = defaultdict(list)

    for category_index, spec in enumerate(CATEGORIES):
        counts = scenario_count_distribution(spec["programs"], spec["tasks"])
        for program_index, scenario_count in enumerate(counts, start=1):
            program_id = f"{spec['prefix']}-{program_index:03d}"
            # Deliberately high synthetic denominators make the generated ratios
            # tunable at the manuscript's displayed precision. They are schema
            # fixtures and must not be interpreted as benchmark measurements.
            original_loc = rng.randint(8000, 12000)
            original_statements = rng.randint(6000, 10000)
            original_cc = rng.randint(4000, 8000)
            program_rows.append(
                {
                    "data_status": STATUS,
                    "program_id": program_id,
                    "category": spec["category"],
                    "category_ordinal": program_index,
                    "scenario_count": scenario_count,
                    "source_status": "SYNTHETIC_IDENTIFIER_ONLY",
                    "source_file": "NOT_INCLUDED",
                }
            )
            for scenario_index in range(1, scenario_count + 1):
                task_id = f"{program_id}-T{scenario_index:02d}"
                testing_condition, defining_condition = illustrative_scenario(
                    spec["category"], scenario_index
                )
                task_row = {
                    "data_status": STATUS,
                    "task_id": task_id,
                    "program_id": program_id,
                    "category": spec["category"],
                    "scenario_index": scenario_index,
                    "testing_condition": testing_condition,
                    "defining_condition": defining_condition,
                }
                task_rows.append(task_row)

                spreads = (Decimal("0.08"), Decimal("0.10"), Decimal("0.09"))
                original_values = (original_loc, original_statements, original_cc)
                slices = []
                for metric_index, (target, spread, original) in enumerate(
                    zip(spec["rq1"], spreads, original_values)
                ):
                    offset = Decimal(str(rng.uniform(-float(spread), float(spread))))
                    ratio = min(Decimal("1"), max(Decimal("0.05"), target + offset))
                    slices.append(max(1, min(original, int((Decimal(original) * ratio).to_integral_value()))))
                rq1_row = {
                    "data_status": STATUS,
                    "task_id": task_id,
                    "program_id": program_id,
                    "category": spec["category"],
                    "original_loc": original_loc,
                    "slice_loc": slices[0],
                    "loc_ratio": "",
                    "original_executable_statements": original_statements,
                    "slice_executable_statements": slices[1],
                    "executable_statement_ratio": "",
                    "original_cyclomatic_complexity": original_cc,
                    "slice_cyclomatic_complexity": slices[2],
                    "cyclomatic_complexity_ratio": "",
                }
                rq1_rows.append(rq1_row)
                tasks_by_category[spec["category"]].append(rq1_row)

    for spec in CATEGORIES:
        category_rows = tasks_by_category[spec["category"]]
        adjust_integer_ratios(category_rows, "original_loc", "slice_loc", spec["rq1"][0])
        adjust_integer_ratios(
            category_rows,
            "original_executable_statements",
            "slice_executable_statements",
            spec["rq1"][1],
        )
        adjust_integer_ratios(
            category_rows,
            "original_cyclomatic_complexity",
            "slice_cyclomatic_complexity",
            spec["rq1"][2],
        )

    for row in rq1_rows:
        row["loc_ratio"] = f"{int(row['slice_loc']) / int(row['original_loc']):.6f}"
        row["executable_statement_ratio"] = (
            f"{int(row['slice_executable_statements']) / int(row['original_executable_statements']):.6f}"
        )
        row["cyclomatic_complexity_ratio"] = (
            f"{int(row['slice_cyclomatic_complexity']) / int(row['original_cyclomatic_complexity']):.6f}"
        )

    rq2_rows: list[dict[str, object]] = []
    task_index_by_category: dict[str, int] = defaultdict(int)
    ratios_by_category = {
        spec["category"]: [
            centered_ratios(target, spec["tasks"], salt=metric_index + category_index * 7)
            for metric_index, target in enumerate(spec["rq2"])
        ]
        for category_index, spec in enumerate(CATEGORIES)
    }
    for task in task_rows:
        category = str(task["category"])
        category_index = next(i for i, item in enumerate(CATEGORIES) if item["category"] == category)
        task_position = task_index_by_category[category]
        task_index_by_category[category] += 1
        dynamic_ratio, path_ratio, smt_ratio, total_ratio = [
            ratios_by_category[category][metric_index][task_position] for metric_index in range(4)
        ]
        base_dynamic = Decimal(str(42 + (task_position * 19 + category_index * 11) % 95))
        base_path = Decimal(str(55 + (task_position * 23 + category_index * 17) % 125))
        base_smt = Decimal(str(38 + (task_position * 29 + category_index * 7) % 110))
        for repetition in range(1, 11):
            jitter = Decimal("1") + Decimal(((repetition * 13 + task_position * 3) % 9) - 4) / Decimal("100")
            original_dynamic = base_dynamic * jitter
            original_path = base_path * jitter
            original_smt = base_smt * jitter
            original_component_sum = original_dynamic + original_path + original_smt
            original_other = original_component_sum * Decimal("0.35")
            original_total = original_component_sum + original_other
            slice_dynamic = original_dynamic * dynamic_ratio
            slice_path = original_path * path_ratio
            slice_smt = original_smt * smt_ratio
            slice_total = original_total * total_ratio
            slicing = original_total * (Decimal("0.025") + Decimal(category_index) / Decimal("1000"))
            slice_other = slice_total - slice_dynamic - slice_path - slice_smt - slicing
            if slice_other <= 0:
                raise RuntimeError(f"Non-positive synthetic other time for {task['task_id']}")
            rq2_rows.append(
                {
                    "data_status": STATUS,
                    "task_id": task["task_id"],
                    "program_id": task["program_id"],
                    "category": category,
                    "repetition": repetition,
                    "original_dynamic_ms": f"{original_dynamic:.6f}",
                    "slice_dynamic_ms": f"{slice_dynamic:.6f}",
                    "dynamic_ratio": f"{dynamic_ratio:.6f}",
                    "original_path_derivation_ms": f"{original_path:.6f}",
                    "slice_path_derivation_ms": f"{slice_path:.6f}",
                    "path_derivation_ratio": f"{path_ratio:.6f}",
                    "original_smt_ms": f"{original_smt:.6f}",
                    "slice_smt_ms": f"{slice_smt:.6f}",
                    "smt_ratio": f"{smt_ratio:.6f}",
                    "original_other_ms": f"{original_other:.6f}",
                    "slice_slicing_ms": f"{slicing:.6f}",
                    "slice_other_ms": f"{slice_other:.6f}",
                    "original_total_ms": f"{original_total:.6f}",
                    "slice_total_ms": f"{slice_total:.6f}",
                    "total_ratio": f"{total_ratio:.6f}",
                }
            )

    rq3_rows: list[dict[str, object]] = []
    grouped_tasks: dict[str, list[dict[str, object]]] = defaultdict(list)
    for task in task_rows:
        grouped_tasks[str(task["category"])].append(task)
    reasons = [
        "MALFORMED_FSF",
        "UNSUPPORTED_SYMBOL",
        "EXPRESSION_TRANSLATION_ERROR",
        "TOOL_EXCEPTION",
    ]
    for category_index, spec in enumerate(CATEGORIES):
        category_tasks = grouped_tasks[spec["category"]]
        for task_position, task in enumerate(category_tasks):
            conclusive = task_position < spec["definite"]
            if conclusive:
                soundness = "SOUND" if (task_position + category_index) % 4 else "UNSOUND"
                completeness = "COMPLETE" if (task_position + category_index) % 5 else "INCOMPLETE"
                reason = ""
            else:
                soundness = "INCONCLUSIVE"
                completeness = "INCONCLUSIVE"
                reason = reasons[(task_position - spec["definite"]) % len(reasons)]
            rq3_rows.append(
                {
                    "data_status": STATUS,
                    "task_id": task["task_id"],
                    "program_id": task["program_id"],
                    "category": spec["category"],
                    "original_availability": "DEFINITE" if conclusive else "INCONCLUSIVE",
                    "slice_availability": "DEFINITE" if conclusive else "INCONCLUSIVE",
                    "original_soundness": soundness,
                    "slice_soundness": soundness,
                    "original_completeness": completeness,
                    "slice_completeness": completeness,
                    "soundness_agreement": "TRUE" if conclusive else "NOT_APPLICABLE",
                    "completeness_agreement": "TRUE" if conclusive else "NOT_APPLICABLE",
                    "inconclusive_reason": reason,
                }
            )

    write_csv(
        SYNTHETIC_DIR / "program_manifest.csv",
        [
            "data_status",
            "program_id",
            "category",
            "category_ordinal",
            "scenario_count",
            "source_status",
            "source_file",
        ],
        program_rows,
    )
    write_csv(
        SYNTHETIC_DIR / "task_manifest.csv",
        [
            "data_status",
            "task_id",
            "program_id",
            "category",
            "scenario_index",
            "testing_condition",
            "defining_condition",
        ],
        task_rows,
    )
    write_csv(
        SYNTHETIC_DIR / "rq1_scale.csv",
        [
            "data_status",
            "task_id",
            "program_id",
            "category",
            "original_loc",
            "slice_loc",
            "loc_ratio",
            "original_executable_statements",
            "slice_executable_statements",
            "executable_statement_ratio",
            "original_cyclomatic_complexity",
            "slice_cyclomatic_complexity",
            "cyclomatic_complexity_ratio",
        ],
        rq1_rows,
    )
    write_csv(
        SYNTHETIC_DIR / "rq2_timing_runs.csv",
        [
            "data_status",
            "task_id",
            "program_id",
            "category",
            "repetition",
            "original_dynamic_ms",
            "slice_dynamic_ms",
            "dynamic_ratio",
            "original_path_derivation_ms",
            "slice_path_derivation_ms",
            "path_derivation_ratio",
            "original_smt_ms",
            "slice_smt_ms",
            "smt_ratio",
            "original_other_ms",
            "slice_slicing_ms",
            "slice_other_ms",
            "original_total_ms",
            "slice_total_ms",
            "total_ratio",
        ],
        rq2_rows,
    )
    write_csv(
        SYNTHETIC_DIR / "rq3_preservation.csv",
        [
            "data_status",
            "task_id",
            "program_id",
            "category",
            "original_availability",
            "slice_availability",
            "original_soundness",
            "slice_soundness",
            "original_completeness",
            "slice_completeness",
            "soundness_agreement",
            "completeness_agreement",
            "inconclusive_reason",
        ],
        rq3_rows,
    )

    metadata = {
        "data_status": STATUS,
        "empirical": False,
        "purpose": "Repository schema, documentation, and validator review only",
        "generator": "scripts/generate_synthetic_preview.py",
        "seed": SEED,
        "program_count": len(program_rows),
        "task_count": len(task_rows),
        "rq2_repetitions_per_task": 10,
        "warning": "Do not cite these generated records as experimental evidence.",
    }
    (SYNTHETIC_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    write_reported_summaries()
    print(f"Generated {len(program_rows)} programs, {len(task_rows)} tasks, and {len(rq2_rows)} timing rows.")


def write_reported_summaries() -> None:
    rq1_rows = []
    rq2_rows = []
    rq3_rows = []
    for spec in CATEGORIES:
        rq1_rows.append(
            {
                "category": spec["category"],
                "programs": spec["programs"],
                "tasks": spec["tasks"],
                "average_fsfs": f"{Decimal(spec['tasks']) / Decimal(spec['programs']):.2f}",
                "loc_ratio": f"{spec['rq1'][0]:.4f}",
                "executable_statement_ratio": f"{spec['rq1'][1]:.4f}",
                "cyclomatic_complexity_ratio": f"{spec['rq1'][2]:.4f}",
                "source": "MANUSCRIPT_TABLE_2",
            }
        )
        rq2_rows.append(
            {
                "category": spec["category"],
                "programs": spec["programs"],
                "tasks": spec["tasks"],
                "dynamic_execution_ratio": f"{spec['rq2'][0]:.3f}",
                "path_derivation_ratio": f"{spec['rq2'][1]:.3f}",
                "smt_solving_ratio": f"{spec['rq2'][2]:.3f}",
                "total_time_ratio": f"{spec['rq2'][3]:.3f}",
                "source": "MANUSCRIPT_TABLE_3",
            }
        )
        rq3_rows.append(
            {
                "category": spec["category"],
                "programs": spec["programs"],
                "tasks": spec["tasks"],
                "definite_pairs": spec["definite"],
                "inconclusive_pairs": spec["inconclusive"],
                "conclusive_preservation_pct": f"{Decimal(spec['definite']) / Decimal(spec['tasks']) * 100:.2f}",
                "soundness_agreement_pct": "100.00",
                "completeness_agreement_pct": "100.00",
                "source": "MANUSCRIPT_TABLE_4",
            }
        )
    rq1_rows.append(
        {
            "category": "Overall",
            "programs": 250,
            "tasks": 740,
            "average_fsfs": "2.96",
            "loc_ratio": f"{RQ1_OVERALL[0]:.4f}",
            "executable_statement_ratio": f"{RQ1_OVERALL[1]:.4f}",
            "cyclomatic_complexity_ratio": f"{RQ1_OVERALL[2]:.4f}",
            "source": "MANUSCRIPT_TABLE_2",
        }
    )
    rq2_rows.append(
        {
            "category": "Overall",
            "programs": 250,
            "tasks": 740,
            "dynamic_execution_ratio": f"{RQ2_OVERALL[0]:.3f}",
            "path_derivation_ratio": f"{RQ2_OVERALL[1]:.3f}",
            "smt_solving_ratio": f"{RQ2_OVERALL[2]:.3f}",
            "total_time_ratio": f"{RQ2_OVERALL[3]:.3f}",
            "source": "MANUSCRIPT_TABLE_3",
        }
    )
    rq3_rows.append(
        {
            "category": "Overall",
            "programs": 250,
            "tasks": 740,
            "definite_pairs": 718,
            "inconclusive_pairs": 22,
            "conclusive_preservation_pct": "97.03",
            "soundness_agreement_pct": "100.00",
            "completeness_agreement_pct": "100.00",
            "source": "MANUSCRIPT_TABLE_4",
        }
    )
    write_csv(
        REPORTED_DIR / "rq1_category_summary.csv",
        [
            "category",
            "programs",
            "tasks",
            "average_fsfs",
            "loc_ratio",
            "executable_statement_ratio",
            "cyclomatic_complexity_ratio",
            "source",
        ],
        rq1_rows,
    )
    write_csv(
        REPORTED_DIR / "rq2_category_summary.csv",
        [
            "category",
            "programs",
            "tasks",
            "dynamic_execution_ratio",
            "path_derivation_ratio",
            "smt_solving_ratio",
            "total_time_ratio",
            "source",
        ],
        rq2_rows,
    )
    write_csv(
        REPORTED_DIR / "rq3_category_summary.csv",
        [
            "category",
            "programs",
            "tasks",
            "definite_pairs",
            "inconclusive_pairs",
            "conclusive_preservation_pct",
            "soundness_agreement_pct",
            "completeness_agreement_pct",
            "source",
        ],
        rq3_rows,
    )


if __name__ == "__main__":
    generate()
