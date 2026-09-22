from __future__ import annotations
from dataclasses import asdict
import hashlib
import json
import platform
import os
from pathlib import Path
import subprocess
import tempfile
import time

import z3
from . import __version__
from .errors import FSFValidationError
from .expression import effective_bounds
from .java_frontend import parse_java
from .models import FSFSpec
from .preservation import compare_judgments, check_preservation
from .report import issues_to_dict, scenario_to_dict, slice_to_dict, write_reports
from .slicer import FSFGuidedSlicer, compile_slice, SliceResult, metrics_for_source
from .tbfv import TBFVEngine, inconclusive
from .validation import reconcile_spec, validate_fsf


def compile_program(program):
    with tempfile.TemporaryDirectory(prefix='fsf-javac-') as directory:
        path = Path(directory) / f'{program.class_name}.java'
        path.write_text(program.source, encoding='utf-8')
        metrics = metrics_for_source(program.source, program.method_name)
        result = compile_slice(SliceResult('', program.source, path, set(), set(), {}, metrics, metrics))
        return {'ok': result.compile_ok, 'message': result.compile_message}


def runtime_metadata():
    try:
        javac = subprocess.run(['javac', '-version'], capture_output=True, text=True, timeout=10)
        compiler = (javac.stdout + javac.stderr).strip()
    except (OSError, subprocess.TimeoutExpired): compiler = 'unavailable'
    return {'python': platform.python_version(), 'platform': platform.platform(),
            'machine': platform.machine(), 'cpu_count': os.cpu_count(), 'z3': z3.get_version_string(), 'javac': compiler}


def _load(java_path, fsf_path):
    spec = FSFSpec.load(fsf_path)
    program = parse_java(java_path, spec.method)
    reconcile_spec(program, spec)
    validation = validate_fsf(program, spec)
    return program, spec, validation


def _domain(spec):
    return {n: {'type': v.type, 'min': effective_bounds(v, spec.config)[0], 'max': effective_bounds(v, spec.config)[1]} for n, v in spec.inputs.items()}


def analyze(java_path, fsf_path, output_dir, force=False):
    started = time.perf_counter()
    program, spec, validation = _load(java_path, fsf_path)
    if not validation.valid and not force:
        raise FSFValidationError('; '.join(i.message for i in validation.issues if i.severity == 'error'))
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    payload = {'tool': 'FSF-Slicer-TBFV', 'version': __version__,
               'program': str(Path(java_path).resolve()), 'fsf': str(Path(fsf_path).resolve()),
               'method': program.method_name, 'analysis_domain': _domain(spec),
               'configuration': asdict(spec.config), 'limits': asdict(spec.config),
               'semantic_model': 'Java scalar integers and Booleans; observations projected to outputs used by D',
               'source_sha256': hashlib.sha256(program.source.encode()).hexdigest(),
               'fsf_sha256': hashlib.sha256(Path(fsf_path).read_bytes()).hexdigest(),
               'environment': runtime_metadata(), 'metadata': spec.metadata,
               'validation': issues_to_dict(validation.issues), 'slices': {}, 'sliced_results': {},
               'original_results': {}, 'comparison': {}}
    if not validation.valid:
        for scenario in spec.scenarios:
            payload['sliced_results'][scenario.id] = scenario_to_dict(inconclusive(scenario.id, 'INVALID_FSF: validation errors prevent verification.'))
        return _finish(payload, root, started)
    compile_started = time.perf_counter()
    compilation = compile_program(program) if spec.config.compile_slices else {'ok': None, 'message': 'Compilation disabled.'}
    payload['original_compilation'] = compilation
    payload['original_compile_ms'] = (time.perf_counter() - compile_started) * 1000
    graph_started = time.perf_counter()
    slicer = FSFGuidedSlicer(program, spec)
    payload['graph_construction_ms'] = (time.perf_counter() - graph_started) * 1000
    if slicer.pdg:
        _write_graph(slicer.pdg, root)
    original_engine = TBFVEngine(program, spec) if spec.config.compare_original or spec.config.check_preservation else None
    for scenario in spec.scenarios:
        slice_result = slicer.slice(scenario, root / 'slices')
        if spec.config.compile_slices: compile_slice(slice_result)
        payload['slices'][scenario.id] = slice_to_dict(slice_result)
        original = None
        if original_engine:
            original = original_engine.verify(scenario) if compilation['ok'] is not False else inconclusive(scenario.id, 'ORIGINAL_COMPILE_FAILED: ' + compilation['message'])
            payload['original_results'][scenario.id] = scenario_to_dict(original)
        if compilation['ok'] is False:
            sliced = inconclusive(scenario.id, 'ORIGINAL_COMPILE_FAILED: ' + compilation['message'])
        elif slice_result.compile_ok is False:
            sliced = inconclusive(scenario.id, 'SLICE_COMPILE_FAILED: ' + slice_result.compile_message)
        else:
            sliced_program = parse_java(slice_result.output_path, spec.method)
            sliced = TBFVEngine(sliced_program, spec).verify(scenario)
        payload['sliced_results'][scenario.id] = scenario_to_dict(sliced)
        comparison = {'judgment_agreement': compare_judgments(original, sliced)}
        if original is not None and spec.config.check_preservation:
            comparison['behavior'] = check_preservation(program, spec, scenario, original, sliced)
        payload['comparison'][scenario.id] = comparison
    return _finish(payload, root, started)


def _finish(payload, root, started):
    payload['total_elapsed_ms'] = (time.perf_counter() - started) * 1000
    json_path, html_path = write_reports(payload, root)
    payload['report_json'], payload['report_html'] = str(json_path), str(html_path)
    return payload


def _write_graph(pdg, root):
    nodes = [{'id': i, 'kind': n.kind, 'line': n.line, 'text': n.text, 'defs': sorted(n.defs), 'uses': sorted(n.uses)} for i, n in pdg.nodes.items()]
    graph = {'nodes': nodes, 'cfg_edges': [[a, b] for a, targets in pdg.cfg.edges.items() for b in sorted(targets)],
             'data_edges': sorted(pdg.data_edges), 'control_edges': sorted(pdg.control_edges)}
    (root / 'dependence-graph.json').write_text(json.dumps(graph, indent=2), encoding='utf-8')
    lines = ['digraph PDG {']
    for n in nodes:
        lines.append(f'  n{n["id"]} [label={json.dumps(str(n["id"]) + ": " + n["text"])}];')
    for kind, style in [('data_edges', 'solid'), ('control_edges', 'dashed')]:
        for a, b in graph[kind]: lines.append(f'  n{a} -> n{b} [style={style}];')
    (root / 'dependence-graph.dot').write_text('\n'.join([*lines, '}']) + '\n', encoding='utf-8')


def slice_only(java_path, fsf_path, output_dir):
    program, spec, report = _load(java_path, fsf_path)
    if not report.valid: raise FSFValidationError('FSF validation failed; run validate-fsf for details.')
    slicer = FSFGuidedSlicer(program, spec)
    results = []
    for scenario in spec.scenarios:
        result = slicer.slice(scenario, output_dir)
        if spec.config.compile_slices: compile_slice(result)
        results.append(slice_to_dict(result))
    return results


def verify_only(java_path, fsf_path):
    program, spec, report = _load(java_path, fsf_path)
    if not report.valid: raise FSFValidationError('FSF validation failed; run validate-fsf for details.')
    compilation = compile_program(program) if spec.config.compile_slices else {'ok': None}
    if compilation['ok'] is False:
        return [scenario_to_dict(inconclusive(s.id, 'ORIGINAL_COMPILE_FAILED: ' + compilation['message'])) for s in spec.scenarios]
    engine = TBFVEngine(program, spec)
    return [scenario_to_dict(engine.verify(s)) for s in spec.scenarios]
