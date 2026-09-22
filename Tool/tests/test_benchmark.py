from fsf_tool.benchmark import cluster_interval, run_benchmark
import yaml
from test_regressions import fixture


def test_cluster_bootstrap_keeps_programs_together():
    rows = [{'program_id':'a','x':1}, {'program_id':'a','x':3}, {'program_id':'b','x':8}]
    a = cluster_interval(rows, 'x', seed=7)
    assert a == cluster_interval(rows, 'x', seed=7)
    assert a['mean'] == 4
    assert a['ci95'][0] <= 4 <= a['ci95'][1]
    assert cluster_interval(rows[:2], 'x')['ci95'] is None


def test_benchmark_failures_are_reported(tmp_path):
    manifest=tmp_path/'manifest.yaml'
    manifest.write_text(yaml.safe_dump({'tasks':[{'id':'missing','java':'missing.java','fsf':'missing.yaml'}]}))
    result=run_benchmark(manifest,tmp_path/'out',repeats=1)
    assert len(result['failures']) == 1
    assert result['rows'] == 0
