from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

from .errors import FSFToolError
from .java_frontend import JavaProgram


def suggest_fsf(
    program: JavaProgram,
    output_path: str | Path,
    model: str,
    base_url: str,
    api_key_env: str = "FSF_LLM_API_KEY",
) -> Path:
    """Optional OpenAI-compatible helper. Formal validation remains local."""
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise FSFToolError(f"Set {api_key_env}; API keys are never stored by this tool.")
    schema = {
        "method": program.method_name,
        "inputs": {name: {"type": kind, "min": -100, "max": 100} for name, kind in program.parameters.items()},
        "outputs": {"return_value": {"type": program.return_type, "source": "return"}},
        "scenarios": [{"id": "T1", "T": "Java boolean expression over inputs", "D": "Java boolean expression including return_value"}],
    }
    prompt = (
        "Derive a mutually input-exclusive and input-complete Functional Scenario Form for the scalar Java method. "
        "Use only Java expression syntax supported by Z3: arithmetic, comparisons, &&, ||, !, %, ternary, Math.abs/min/max. "
        "Return JSON only, following this shape:\n"
        + json.dumps(schema)
        + "\nJava source:\n```java\n"
        + program.source
        + "\n```"
    )
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0}).encode()
    endpoint = base_url.rstrip("/")
    if not endpoint.endswith("/chat/completions"):
        endpoint += "/chat/completions"
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = payload["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        raise FSFToolError(f"LLM request failed: {exc}") from exc
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0]
        if content.lstrip().startswith("json"):
            content = content.lstrip()[4:].lstrip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise FSFToolError(f"LLM did not return valid JSON: {exc}") from exc
    target = Path(output_path)
    target.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return target

