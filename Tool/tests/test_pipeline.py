from pathlib import Path

from fsf_tool.pipeline import analyze


ROOT = Path(__file__).resolve().parents[1]


def test_calculator_pipeline(tmp_path):
    result = analyze(ROOT / "examples/Calculator.java", ROOT / "examples/calculator.fsf.yaml", tmp_path)
    for scenario in result["sliced_results"].values():
        assert scenario["soundness"]["status"] == "sound"
        assert scenario["completeness"]["status"] == "complete"
    assert all(item["compile_ok"] for item in result["slices"].values())
    assert (tmp_path / "report.html").exists()


def test_loop_pipeline(tmp_path):
    result = analyze(ROOT / "examples/UserInputProgram.java", ROOT / "examples/cube_sum.fsf.yaml", tmp_path)
    assert result["sliced_results"]["T_nonpositive"]["soundness"]["status"] == "sound"
    assert result["sliced_results"]["T_positive"]["soundness"]["status"] in {"sound", "locally_sound"}


def test_bundled_dataset_branch_and_loop(tmp_path):
    fizz = analyze(
        ROOT / "datasets/PCaE-Dataset/Branched3/FizzBuzz_Original.java",
        ROOT / "examples/dataset_fizzbuzz.fsf.yaml",
        tmp_path / "fizz",
    )
    assert all(item["soundness"]["status"] == "sound" for item in fizz["sliced_results"].values())
    multiply = analyze(
        ROOT / "datasets/PCaE-Dataset/Nested-Loop3/MulLoop_Original.java",
        ROOT / "examples/dataset_mul_loop.fsf.yaml",
        tmp_path / "multiply",
    )
    assert all(item["soundness"]["status"] == "sound" for item in multiply["sliced_results"].values())
    assert all(item["compile_ok"] for item in multiply["slices"].values())
