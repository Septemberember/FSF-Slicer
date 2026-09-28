#!/usr/bin/env python3
"""Run the four paper specification alternatives independently, with fresh evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml
from fsf_tool.pipeline import analyze

LOWER = '((return_value - 1) * (return_value - 1) * return_value * return_value) / 4'
UPPER = '(return_value * return_value * (return_value + 1) * (return_value + 1)) / 4'
OPERATORS = [('<', '<='), ('<=', '<='), ('<', '<'), ('<=', '<')]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upper-bound', type=int, choices=[500, 784, 800], default=784)
    parser.add_argument('--output', type=Path, default=Path('cube-table-output'))
    args = parser.parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    summary = {'input_upper_bound': args.upper_bound,
               'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
               'measurement_note': 'Fresh single runs; these are not the historical paper timings.',
               'rows': []}
    for row, (lower, upper) in enumerate(OPERATORS, 1):
        spec = yaml.safe_load((ROOT / 'examples/cube_sum.fsf.yaml').read_text())
        spec['inputs']['x']['max'] = args.upper_bound
        spec['scenarios'][1]['D'] = f'{LOWER} {lower} x && x {upper} {UPPER}'
        spec['metadata'] = {'paper_table': 1, 'row': row, 'independent_specification_variant': True}
        directory = args.output / f'row-{row}'
        directory.mkdir(parents=True, exist_ok=True)
        fsf = directory / 'spec.fsf.yaml'
        fsf.write_text(yaml.safe_dump(spec, sort_keys=False), encoding='utf-8')
        report = analyze(ROOT / 'examples/UserInputProgram.java', fsf, directory)
        result = report['sliced_results']['T_positive']
        original = report['original_results']['T_positive']
        summary['rows'].append({
            'row': row, 'D': spec['scenarios'][1]['D'],
            'soundness': result['soundness'], 'completeness': result['completeness'],
            'original_soundness': original['soundness'], 'original_completeness': original['completeness'],
            'coverage': result['coverage'], 'positive_paths': len(result['paths']),
            'test_generation_checks_both_scenarios': sum(
                s['test_generation_checks'] for s in report['sliced_results'].values()),
            'tests': [p['test_case'] for p in result['paths']],
            'comparison': report['comparison']['T_positive'],
            'source_sha256': report['source_sha256'], 'fsf_sha256': report['fsf_sha256'],
            'environment': report['environment'], 'tool_version': report['version'],
            'total_elapsed_ms': report['total_elapsed_ms'],
            'report': f'row-{row}/report.json',
        })
        print(f"Row {row}: {result['soundness']['status']} / {result['completeness']['status']}; "
              f"{len(result['paths'])} positive paths", flush=True)
    target = args.output / 'summary.json'
    target.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(target)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
