from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from .models import ScenarioResult, ValidationIssue
from .slicer import SliceResult


def scenario_to_dict(result: ScenarioResult) -> dict[str, Any]:
    return {
        "scenario_id": result.scenario_id,
        "soundness": judgment_to_dict(result.soundness),
        "completeness": judgment_to_dict(result.completeness),
        "coverage": result.coverage,
        "elapsed_ms": round(result.elapsed_ms, 3),
        "warnings": result.warnings,
        "paths": [
            {
                "index": path.index,
                "test_case": path.test_case,
                "path_condition": path.path_condition_text,
                "outputs": path.output_text,
                "trace": path.trace,
                "loop_iterations": path.loop_iterations,
                "truncated": path.truncated,
                "exception": path.exception,
            }
            for path in result.paths
        ],
    }


def judgment_to_dict(value: Any) -> dict[str, Any]:
    return {"status": value.status, "reason": value.reason, "counterexample": value.counterexample}


def slice_to_dict(result: SliceResult) -> dict[str, Any]:
    return {
        "scenario_id": result.scenario_id,
        "output_path": str(result.output_path) if result.output_path else None,
        "kept_nodes": len(result.kept_node_ids),
        "removed_nodes": len(result.removed_node_ids),
        "pruned_branches": len(result.pruned_branches),
        "original_metrics": result.original_metrics.as_dict(),
        "slice_metrics": result.slice_metrics.as_dict(),
        "compile_ok": result.compile_ok,
        "compile_message": result.compile_message,
        "warnings": result.warnings,
    }


def write_reports(payload: dict[str, Any], output_dir: str | Path) -> tuple[Path, Path]:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    json_path = folder / "report.json"
    html_path = folder / "report.html"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    html_path.write_text(render_html(payload), encoding="utf-8")
    return json_path, html_path


def render_html(payload: dict[str, Any]) -> str:
    title = html.escape(payload.get("program", "FSF-TBFV report"))
    validation_rows = "".join(
        f"<tr><td>{_e(item['severity'])}</td><td>{_e(item['code'])}</td><td>{_e(item['message'])}</td><td><code>{_e(json.dumps(item.get('counterexample'), ensure_ascii=False))}</code></td></tr>"
        for item in payload.get("validation", [])
    ) or '<tr><td colspan="4">No validation issues</td></tr>'
    cards = []
    scenario_sections = []
    sliced_results = payload.get("sliced_results", {})
    original_results = payload.get("original_results", {})
    slices = payload.get("slices", {})
    for scenario_id, result in sliced_results.items():
        sound = result["soundness"]["status"]
        complete = result["completeness"]["status"]
        cards.append(
            f'<article class="card"><h3>{_e(scenario_id)}</h3><p><span class="badge {sound}">{_e(sound)}</span> '
            f'<span class="badge {complete}">{_e(complete)}</span></p><p>{len(result["paths"])} paths · {_e(result["coverage"])} coverage</p></article>'
        )
        path_rows = "".join(
            f"<tr><td>{path['index']}</td><td><code>{_e(json.dumps(path['test_case'], ensure_ascii=False))}</code></td>"
            f"<td><code>{_e(path['path_condition'])}</code></td><td><code>{_e(json.dumps(path['outputs'], ensure_ascii=False))}</code></td>"
            f"<td>{_e(path.get('exception') or '')}</td></tr>"
            for path in result["paths"]
        )
        slice_info = slices.get(scenario_id, {})
        metrics = slice_info.get("slice_metrics", {})
        original_metrics = slice_info.get("original_metrics", {})
        original = original_results.get(scenario_id)
        preservation = "not compared"
        if original:
            preservation = (
                "preserved"
                if original["soundness"]["status"] == sound and original["completeness"]["status"] == complete
                else "different/inconclusive"
            )
        scenario_sections.append(
            f"<section><h2>{_e(scenario_id)}</h2>"
            f"<p><b>Soundness:</b> {_e(sound)} — {_e(result['soundness']['reason'])}</p>"
            f"<p><b>Completeness:</b> {_e(complete)} — {_e(result['completeness']['reason'])}</p>"
            f"<p><b>Slice:</b> LOC {original_metrics.get('loc','?')} → {metrics.get('loc','?')}, statements {original_metrics.get('executable_statements','?')} → {metrics.get('executable_statements','?')}, complexity {original_metrics.get('cyclomatic_complexity','?')} → {metrics.get('cyclomatic_complexity','?')}; compile={_e(slice_info.get('compile_ok'))}; original/slice={_e(preservation)}</p>"
            f"<table><thead><tr><th>#</th><th>Test case</th><th>Path condition C</th><th>State representation</th><th>Exception</th></tr></thead><tbody>{path_rows}</tbody></table></section>"
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · FSF-Slicer-TBFV</title>
<style>
:root{{--ink:#172033;--muted:#5d687c;--paper:#f4f7fb;--card:#fff;--line:#dbe3ef;--accent:#3157d5;--good:#147d64;--warn:#b46a00;--bad:#be3345}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.55 Inter,ui-sans-serif,system-ui,sans-serif}}main{{max-width:1200px;margin:0 auto;padding:36px 24px 72px}}h1{{font-size:32px;margin:0}}h2{{margin-top:42px}}.lede{{color:var(--muted);margin:6px 0 24px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}}.card,section{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;box-shadow:0 4px 18px #25365a0a}}section{{overflow:auto}}table{{width:100%;border-collapse:collapse;margin-top:14px}}th,td{{border-bottom:1px solid var(--line);padding:9px;text-align:left;vertical-align:top}}code{{white-space:pre-wrap;word-break:break-word;font-size:12px}}.badge{{display:inline-block;padding:3px 8px;border-radius:999px;background:#e8edf9}}.sound,.complete{{background:#dff5ed;color:var(--good)}}.unsound,.incomplete{{background:#fde4e7;color:var(--bad)}}.locally_sound,.locally_complete,.inconclusive{{background:#fff0d5;color:var(--warn)}}
</style></head><body><main><h1>{title}</h1><p class="lede">FSF-guided slicing and testing-based formal verification report</p>
<div class="grid">{''.join(cards)}</div><h2>FSF validation</h2><section><table><thead><tr><th>Severity</th><th>Code</th><th>Message</th><th>Counterexample</th></tr></thead><tbody>{validation_rows}</tbody></table></section>
{''.join(scenario_sections)}</main></body></html>"""


def _e(value: Any) -> str:
    return html.escape(str(value))


def issues_to_dict(issues: list[ValidationIssue]) -> list[dict[str, Any]]:
    return [
        {"severity": issue.severity, "code": issue.code, "message": issue.message, "counterexample": issue.counterexample}
        for issue in issues
    ]

