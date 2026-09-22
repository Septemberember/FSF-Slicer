"""Paired runs and program-cluster bootstrap intervals; no historical data synthesis."""
from __future__ import annotations
import csv
from dataclasses import asdict
import json
from pathlib import Path
import random
import statistics

import yaml
from .errors import FSFToolError
from .models import FSFSpec, FunctionalScenario, _UniqueLoader, _fields
from .pipeline import analyze, runtime_metadata


def cluster_interval(rows, value_key, seed=0, draws=2000):
    groups = {}
    for row in rows:
        value = row.get(value_key)
        if value is not None: groups.setdefault(row['program_id'], []).append(float(value))
    if not groups: return {'mean': None, 'ci95': None, 'programs': 0}
    values = list(groups.values())
    mean = statistics.mean(x for group in values for x in group)
    if len(values) < 2: return {'mean': mean, 'ci95': None, 'programs': len(values)}
    rng = random.Random(seed)
    samples = []
    for _ in range(draws):
        sample = [x for _ in values for x in rng.choice(values)]
        samples.append(statistics.mean(sample))
    samples.sort()
    return {'mean': mean, 'ci95': [samples[int(.025 * draws)], samples[min(draws-1, int(.975 * draws))]], 'programs': len(values)}


def run_benchmark(manifest_path, output_dir, repeats=10, seed=0, modes=('fsf',)):
    if repeats < 1 or repeats > 1000: raise FSFToolError('repeats must be in [1,1000].')
    if not modes or len(set(modes)) != len(modes) or set(modes) - {'fsf', 'backward', 'conditioned'}:
        raise FSFToolError('modes must be distinct values: fsf, backward, conditioned.')
    source = Path(manifest_path).resolve()
    raw = yaml.load(source.read_text(encoding='utf-8'), Loader=_UniqueLoader)
    _fields(raw, {'tasks', 'description'}, 'benchmark manifest')
    tasks = raw.get('tasks')
    if not isinstance(tasks, list) or not tasks: raise FSFToolError('Manifest tasks must be a nonempty list.')
    ids = set()
    for task in tasks:
        _fields(task, {'id', 'program_id', 'java', 'fsf'}, 'benchmark task')
        if any(not isinstance(task.get(k), str) or not task[k] for k in ('id', 'java', 'fsf')):
            raise FSFToolError('Each benchmark task needs string id, java and fsf fields.')
        FunctionalScenario(task['id'], 'true', 'true')
        if task['id'].casefold() in ids: raise FSFToolError('Duplicate benchmark task ID.')
        ids.add(task['id'].casefold())
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    rows, failures = [], []
    jobs = [(repeat, mode, task) for repeat in range(repeats) for mode in modes for task in tasks]
    random.Random(seed).shuffle(jobs)
    for repeat, mode, task in jobs:
        folder = root / task['id'] / mode / f'run-{repeat+1:03d}'
        folder.mkdir(parents=True, exist_ok=True)
        try:
            spec = FSFSpec.load(source.parent / task['fsf'])
            spec.config.random_seed = (seed + repeat) % (2**31)
            spec.config.slicing_mode = mode
            spec.config.compare_original = True
            effective = folder / 'effective.fsf.yaml'
            effective.write_text(yaml.safe_dump(spec.to_dict(), sort_keys=False), encoding='utf-8')
            result = analyze(source.parent / task['java'], effective, folder)
            for scenario_id, sliced in result['sliced_results'].items():
                original = result['original_results'][scenario_id]
                info = result['slices'][scenario_id]
                om, sm = info['original_metrics'], info['slice_metrics']
                row = {'program_id': task.get('program_id', task['id']), 'task_id': task['id'],
                       'scenario_id': scenario_id, 'mode': mode, 'repeat': repeat+1, 'seed': spec.config.random_seed,
                       'original_verify_ms': original['elapsed_ms'], 'slice_verify_ms': sliced['elapsed_ms'],
                       'slicing_ms': info['elapsed_ms'], 'graph_ms': result['graph_construction_ms'],
                       'pipeline_ms': result['total_elapsed_ms'], 'compile_ok': info['compile_ok'],
                       'original_soundness': original['soundness']['status'], 'slice_soundness': sliced['soundness']['status'],
                       'original_completeness': original['completeness']['status'], 'slice_completeness': sliced['completeness']['status'],
                       'agreement': result['comparison'][scenario_id]['judgment_agreement'],
                       'behavior': result['comparison'][scenario_id].get('behavior', {}).get('status', 'not_checked'),
                       'original_paths': len(original['paths']), 'slice_paths': len(sliced['paths'])}
                row['paired_verify_delta_ms'] = row['slice_verify_ms'] - row['original_verify_ms']
                # Graph construction is shared equally across the scenarios in one program run.
                row['amortized_slice_total_ms'] = row['slice_verify_ms'] + row['slicing_ms'] + row['graph_ms']/len(result['slices'])
                for metric in ('loc', 'executable_statements', 'cyclomatic_complexity'):
                    row[metric+'_ratio'] = sm[metric]/om[metric] if om[metric] else None
                rows.append(row)
        except Exception as exc:
            failures.append({'task_id': task['id'], 'mode': mode, 'repeat': repeat+1, 'error': f'{type(exc).__name__}: {exc}'})
    rows.sort(key=lambda r: (r['mode'], r['program_id'], r['scenario_id'], r['repeat']))
    if rows:
        with (root/'runs.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    summary = {'environment': runtime_metadata(), 'repeats': repeats, 'seed': seed, 'rows': len(rows), 'failures': failures,
               'aggregation': 'Scenario-level paired rows; percentile 95% bootstrap resamples whole programs, retaining their scenarios and repetitions. Timing deltas are slice minus original. Timings are milliseconds. Compilation and report generation are included only in pipeline_ms.', 'modes': {}}
    for mode in modes:
        group = [r for r in rows if r['mode'] == mode]
        summary['modes'][mode] = {key: cluster_interval(group, key, seed) for key in ('paired_verify_delta_ms', 'original_verify_ms', 'slice_verify_ms', 'amortized_slice_total_ms', 'loc_ratio', 'executable_statements_ratio', 'cyclomatic_complexity_ratio')}
        summary['modes'][mode]['conclusive_agreement_rows'] = sum(r['agreement'] == 'agree' for r in group)
        summary['modes'][mode]['inconclusive_rows'] = sum(r['agreement'] == 'inconclusive' for r in group)
        summary['modes'][mode]['behavior_equivalent_rows'] = sum(r['behavior'] == 'equivalent' for r in group)
    (root/'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary
