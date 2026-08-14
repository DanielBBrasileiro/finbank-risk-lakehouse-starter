import shutil
import subprocess

from scripts.doctor import (
    IMPORT_TIMEOUT_SECONDS,
    CheckResult,
    overall_exit_code,
    run_import_check,
    run_tool_check,
)


def test_run_import_check_reports_available_module() -> None:
    result = run_import_check("json", critical=True)

    assert result.name == "python package: json"
    assert result.ok is True
    assert result.critical is True


def test_run_import_check_reports_timeout(monkeypatch) -> None:
    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="python", timeout=IMPORT_TIMEOUT_SECONDS)

    monkeypatch.setattr(subprocess, "run", timeout)

    result = run_import_check("slow_module", critical=True)

    assert result == CheckResult(
        name="python package: slow_module",
        ok=False,
        detail=f"import timed out after {IMPORT_TIMEOUT_SECONDS}s",
        critical=True,
    )


def test_run_tool_check_reports_missing_optional_tool(monkeypatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda _name: None)

    result = run_tool_check("definitely-not-installed", critical=False)

    assert result == CheckResult(
        name="cli tool: definitely-not-installed",
        ok=False,
        detail="not found on PATH",
        critical=False,
    )
    assert overall_exit_code([result]) == 0


def test_overall_exit_code_fails_when_critical_check_fails() -> None:
    result = CheckResult(name="critical", ok=False, detail="broken", critical=True)

    assert overall_exit_code([result]) == 1
