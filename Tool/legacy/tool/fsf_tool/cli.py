from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import javalang
import yaml
import z3

from . import __version__
from .errors import FSFToolError
from .java_frontend import parse_java
from .llm import suggest_fsf
from .models import FSFSpec
from .pipeline import analyze, slice_only
from .report import issues_to_dict, scenario_to_dict
from .tbfv import TBFVEngine
from .validation import reconcile_spec, validate_fsf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fsf-tbfv", description="FSF-guided Java slicing and testing-based formal verification")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    analyze_cmd = commands.add_parser("analyze", help="Run validation, slicing, TBFV, preservation comparison, and reports")
    _io_args(analyze_cmd, output=True)
    analyze_cmd.add_argument("--force", action="store_true", help="Continue despite FSF validation errors (results may be inconclusive)")

    slice_cmd = commands.add_parser("slice", help="Generate and compile one executable slice per scenario")
    _io_args(slice_cmd, output=True)

    verify_cmd = commands.add_parser("verify", help="Run TBFV without slicing")
    _io_args(verify_cmd, output=False)

    validate_cmd = commands.add_parser("validate-fsf", help="Check syntax, variables, T satisfiability, exclusivity, and family coverage")
    _io_args(validate_cmd, output=False)

    init_cmd = commands.add_parser("init-fsf", help="Create an editable FSF YAML scaffold from a Java method")
    init_cmd.add_argument("--java", required=True)
    init_cmd.add_argument("--method")
    init_cmd.add_argument("--output", required=True)

    suggest_cmd = commands.add_parser("suggest-fsf", help="Optionally ask an OpenAI-compatible LLM to draft FSF YAML")
    suggest_cmd.add_argument("--java", required=True)
    suggest_cmd.add_argument("--method")
    suggest_cmd.add_argument("--output", required=True)
    suggest_cmd.add_argument("--model", required=True)
    suggest_cmd.add_argument("--base-url", default="https://api.openai.com/v1")
    suggest_cmd.add_argument("--api-key-env", default="FSF_LLM_API_KEY")
    suggest_cmd.add_argument("--allow-llm", action="store_true", help="Required acknowledgement that source will be sent to the configured API")

    scan_cmd = commands.add_parser("dataset-check", help="Parse all Java files in a dataset and report supported/unsupported methods")
    scan_cmd.add_argument("--java-dir", required=True)
    scan_cmd.add_argument("--output")

    commands.add_parser("doctor", help="Show dependency and runtime readiness")
    return parser


def _io_args(parser: argparse.ArgumentParser, output: bool) -> None:
    parser.add_argument("--java", required=True, help="Target Java source file")
    parser.add_argument("--fsf", required=True, help="FSF YAML file")
    if output:
        parser.add_argument("--output", required=True, help="Output directory")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "analyze":
            result = analyze(args.java, args.fsf, args.output, force=args.force)
            print(json.dumps({"report_json": result["report_json"], "report_html": result["report_html"]}, ensure_ascii=False, indent=2))
        elif args.command == "slice":
            print(json.dumps(slice_only(args.java, args.fsf, args.output), ensure_ascii=False, indent=2))
        elif args.command == "verify":
            spec = FSFSpec.load(args.fsf)
            program = parse_java(args.java, spec.method)
            reconcile_spec(program, spec)
            report = validate_fsf(program, spec)
            if not report.valid:
                raise FSFToolError("FSF validation failed; run validate-fsf for details.")
            print(json.dumps([scenario_to_dict(TBFVEngine(program, spec).verify(s)) for s in spec.scenarios], ensure_ascii=False, indent=2))
        elif args.command == "validate-fsf":
            spec = FSFSpec.load(args.fsf)
            program = parse_java(args.java, spec.method)
            reconcile_spec(program, spec)
            report = validate_fsf(program, spec)
            print(json.dumps({"valid": report.valid, "issues": issues_to_dict(report.issues)}, ensure_ascii=False, indent=2))
            return 0 if report.valid else 2
        elif args.command == "init-fsf":
            _init_fsf(args.java, args.method, args.output)
        elif args.command == "suggest-fsf":
            if not args.allow_llm:
                raise FSFToolError("Pass --allow-llm to confirm that the Java source may be sent to the configured API.")
            program = parse_java(args.java, args.method)
            print(suggest_fsf(program, args.output, args.model, args.base_url, args.api_key_env))
        elif args.command == "dataset-check":
            result = _dataset_check(args.java_dir)
            output = json.dumps(result, ensure_ascii=False, indent=2)
            if args.output:
                Path(args.output).write_text(output, encoding="utf-8")
            print(output)
        elif args.command == "doctor":
            print(json.dumps({
                "tool_version": __version__,
                "python": sys.version.split()[0],
                "z3": z3.get_version_string(),
                "javalang": getattr(javalang, "__version__", "0.13.0"),
                "javac": shutil.which("javac"),
                "ready": shutil.which("javac") is not None,
            }, indent=2))
        return 0
    except (FSFToolError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _init_fsf(java: str, method: str | None, output: str) -> None:
    program = parse_java(java, method)
    data = {
        "method": program.method_name,
        "inputs": {name: {"type": kind, "min": -100, "max": 100} for name, kind in program.parameters.items()},
        "outputs": {"return_value": {"type": program.return_type, "source": "return"}},
        "scenarios": [{"id": "T1", "T": "true", "D": "return_value == 0", "description": "Edit this scenario"}],
        "analysis": {"max_paths": 128, "max_loop_iterations": 128, "solver_timeout_ms": 10000, "compare_original": True, "compile_slices": True},
    }
    Path(output).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(output)


def _dataset_check(folder: str) -> dict[str, object]:
    root = Path(folder)
    files = sorted(root.rglob("*.java"))
    successes = []
    failures = []
    for path in files:
        try:
            program = parse_java(path)
            successes.append({"file": str(path), "class": program.class_name, "method": program.method_name, "inputs": program.parameters, "return": program.return_type})
        except Exception as exc:
            failures.append({"file": str(path), "error": str(exc)})
    return {"root": str(root.resolve()), "total": len(files), "parsed": len(successes), "failed": len(failures), "failures": failures, "programs": successes}


if __name__ == "__main__":
    raise SystemExit(main())

