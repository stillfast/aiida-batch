#!/usr/bin/env python3
"""CLI runner for batch submission workchains (Abacus and VASP).

Reads a YAML (or JSON) config file and submits the workchain to daemon.
By default it spawns a **detached background monitor** that watches the
workflow and auto-generates a report when it finishes.

Supported workchains
--------------------
* ``abacus.base.batch`` — Abacus base (scf) calculations
* ``abacus.band.batch`` — Abacus band calculations
* ``vasp.base.batch`` — VASP base (scf) calculations
* ``vasp.band.batch`` — VASP band calculations

Usage
-----
.. code-block:: bash

    run-batch config.yaml                 # submit + background monitor → report
    run-batch config.yaml --dry-run       # dry-run only
    run-batch config.yaml --local         # run locally (blocking)
    run-batch config.yaml --no-report     # submit only, skip background monitor

Config file structure
---------------------
.. code-block:: yaml

    profile: "my-profile"                     # required — AiiDA profile name
    workchain: "vasp.base.batch"              # required — workchain entry point

    report:                                   # optional — report output settings
      output_dir: "/path/to/reports"
      output_name: "my-batch"                 # final name: my-batch-<PK>.md
      poll_interval: 60                       # poll interval in seconds (default: 60)
      max_poll_time: 86400                    # max total poll time in seconds (optional)

    plot:                                     # optional — DOS/band plotting config
      dos_output_dir: "./dos_plots"
      band_output_dir: "./band_plots"
      xmin: -5
      xmax: 7
      dpi: 150
      pseudo_labels:
        "UO/hl-nr-pbe": "PBE"

    inputs:                                   # passed to the workchain
      structure_config: ...
      potentials_list: ...

Post-processing
---------------
After the workflow finishes, use ``run-post`` for report/plots:

.. code-block:: bash

    run-post <PK> config.yaml --all           # report + dos + band
    run-post <PK> config.yaml --dos           # DOS plots only
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config(path: Path) -> dict:
    """Load a YAML or JSON config file and return as dict."""
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    elif path.suffix == ".json":
        import json
        return json.loads(text)
    else:
        raise ValueError(
            f"Unsupported config file format: {path.suffix} "
            "(supported: .yaml, .yml, .json)"
        )


def _load_profile(cfg: dict) -> None:
    """Load the AiiDA profile from the config (key ``profile``)."""
    from aiida import load_profile
    profile_name = cfg.get("profile")
    load_profile(profile_name) if profile_name else load_profile()


def _parse_name_and_ext(name: str) -> tuple[str, str]:
    """Split a filename into (stem, ext).  ``ext`` includes the dot, e.g. ``.md``.

    If there is no recognised extension, ``.md`` is used as default.
    """
    p = Path(name)
    if p.suffix in (".md", ".markdown", ".html", ".json", ".txt"):
        return p.stem, p.suffix
    return name, ".md"


def build_workchain_inputs(cfg: dict) -> dict:
    """Construct the full inputs dict for a batch workchain.

    Delegates to the workchain class's ``build_inputs_from_config``
    classmethod.  The workchain must already be loaded via
    ``WorkflowFactory``.

    Reads from ``cfg["inputs"]`` — the top-level keys ``profile``,
    ``workchain`` and ``report`` are ignored.
    """
    # Lazy import to avoid circular dependency at module level.
    from aiida_batch.workflows.abacus import (
        AbacusBatchSubmitWorkChain,
    )
    from aiida_batch.workflows.vasp import (
        VaspBatchSubmitWorkChain,
    )

    # Base classes for fallback
    base_classes = (AbacusBatchSubmitWorkChain, VaspBatchSubmitWorkChain)

    workchain_entry_point = cfg.get("workchain", "")
    cls = AbacusBatchSubmitWorkChain
    if workchain_entry_point:
        from aiida.plugins import WorkflowFactory
        try:
            cls = WorkflowFactory(workchain_entry_point)
        except Exception:
            pass  # fall back to base class (minimal set of inputs)

    if hasattr(cls, "build_inputs_from_config"):
        return cls.build_inputs_from_config(cfg)

    # Fallback: generic Dict/List wrappers for batch inputs only.
    from aiida import orm
    inp = cfg.get("inputs", {})
    return {
        "structure_config": orm.Dict(dict=inp.get("structure_config", {})),
        "pseudos_list": orm.List(list=inp.get("pseudos_list", [])),
        "pseudos_max": orm.Int(inp.get("pseudos_max", 99999)),
        "structure_max": orm.Int(inp.get("structure_max", 99999)),
        "dry_run": orm.Bool(inp.get("dry_run", False)),
    }


def _resolve_report_path(cfg: dict, cli_output: str | None, pk: int) -> Path:
    """Determine the report output path.

    Precedence:
      1. ``-o`` CLI argument
      2. ``report.output_dir`` + ``report.output_name`` from config
      3. ``./REPORT-<PK>.md``

    When ``output_name`` has an extension (e.g. ``REPORT.md``) the PK is
    inserted before the extension: ``REPORT-<PK>.md``.
    """
    if cli_output:
        return Path(cli_output).resolve()

    report_cfg = cfg.get("report", {}) or {}
    out_dir = report_cfg.get("output_dir")
    out_name = report_cfg.get("output_name", "REPORT")

    stem, ext = _parse_name_and_ext(out_name)

    if out_dir:
        return (Path(out_dir) / f"{stem}-{pk}{ext}").resolve()
    return Path(f"{stem}-{pk}{ext}").resolve()


# ---------------------------------------------------------------------------
# Background monitor entry point (called as a detached subprocess)
# ---------------------------------------------------------------------------

def _run_background_monitor(config_path: Path, pk: int, output_path: Path,
                            poll: int | None = None) -> None:
    """Load profile, poll for completion, generate report, then exit.
    
    Poll interval and max duration are read from the config file
    (``report.poll_interval`` / ``report.max_poll_time``).
    """
    log_path = (Path.cwd() / f"monitor-{pk}.log").resolve()

    try:
        import sys as _sys

        _sys.stdout = open(log_path, "w", encoding="utf-8")
        _sys.stderr = _sys.stdout

        print(f"[{pk}] Background monitor started at {__import__('datetime').datetime.now()}")
        print(f"[{pk}] config: {config_path}")
        print(f"[{pk}] output: {output_path}")
        _sys.stdout.flush()

        cfg = load_config(config_path)
        _load_profile(cfg)

        report_cfg = cfg.get("report", {}) or {}
        poll_interval = report_cfg.get("poll_interval", 60)
        max_poll_time = report_cfg.get("max_poll_time")

        from aiida_batch.utils.report import monitor_and_report
        result = monitor_and_report(
            pk, config_path, output_path,
            poll_interval=poll_interval,
            max_poll_time=max_poll_time,
        )
        print(f"[{pk}] Report saved to {result}")
    except Exception as exc:
        import traceback
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{pk}] ERROR: {exc}\n")
            traceback.print_exc(file=f)
        return


# ---------------------------------------------------------------------------
# Main / CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run batch submission workchains (Abacus or VASP) from a config file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Supported workchains:\n"
            "  abacus.base.batch, abacus.band.batch\n"
            "  vasp.base.batch, vasp.band.batch\n"
            "\n"
            "Config keys for run:\n"
            "  profile       AiiDA profile name (required)\n"
            "  workchain     Workchain class name (required)\n"
            "  report        Optional — output_dir, output_name, poll_interval, max_poll_time\n"
            "  plot          Optional — dos_output_dir, band_output_dir, xmin, xmax, dpi, pseudo_labels\n"
            "  inputs        Dict forwarded to the workchain\n"
            "\n"
            "Post-processing:\n"
            "  run-post <PK> config.yaml --all    generate report + DOS + band plots"
        ),
    )

    # Internal: spawned by the main process for background monitoring.
    parser.add_argument(
        "--background-monitor",
        dest="background_monitor_pk",
        default=None,
        help=argparse.SUPPRESS,
    )

    parser.add_argument("config", type=Path, help="Path to YAML/JSON config file")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run locally (blocking) instead of submitting to daemon",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Set dry_run=True in the workchain",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip report generation (by default a background monitor is spawned)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output path for the report (default: REPORT-<PK>.md / config.report.*)",
    )
    parser.add_argument(
        "--poll",
        type=int,
        default=60,
        help="Poll interval in seconds for local mode only (default: 60). "
             "For daemon mode, use config key report.poll_interval.",
    )
    args = parser.parse_args()
    config_path = args.config.resolve()

    # ── Background monitor mode (detached subprocess) ──────────
    if args.background_monitor_pk is not None:
        output_path = Path(args.output).resolve() if args.output else Path.cwd() / f"REPORT-{args.background_monitor_pk}.md"
        _run_background_monitor(config_path, int(args.background_monitor_pk),
                                output_path, args.poll)
        return

    # ── Normal mode: load config & profile ────────────────────────
    cfg = load_config(config_path)
    _load_profile(cfg)

    workchain_class = cfg.get("workchain")
    if not workchain_class:
        print("Error: 'workchain' key is required in config (e.g. workchain: vasp.base.batch)", file=sys.stderr)
        sys.exit(1)

    from aiida.plugins import WorkflowFactory
    try:
        WorkChain = WorkflowFactory(workchain_class)
    except Exception as exc:
        print(f"Error: cannot load workchain '{workchain_class}': {exc}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        cfg.setdefault("inputs", {})["dry_run"] = True

    inputs = build_workchain_inputs(cfg)

    # ── --dry-run: run locally, no report ──
    if args.dry_run:
        args.local = True
        args.no_report = True

    # ── Local (blocking) ──────────────────────────────────────────
    if args.local:
        from aiida.engine import run_get_node

        _, node = run_get_node(WorkChain, inputs)

        if "results" in node.outputs:
            results = node.outputs["results"].get_dict()
            children = results.get("children", [])
            n_ok = sum(1 for c in children if c["ok"])
            n_fail = len(children) - n_ok
            print(f"\nResults: {n_ok} OK, {n_fail} failed (total {len(children)})")
            for c in children:
                status = "OK" if c["ok"] else "FAIL"
                print(f"  [{status:4s}] pseudo={c['pseudo']:20s}  proto={c['proto']:8s}  PK={c['pk']}")

        if not args.no_report:
            from aiida_batch.utils.report import generate_report
            output_path = _resolve_report_path(cfg, args.output, node.pk)
            path = generate_report(node.pk, config_path, output_path)
            print(f"Report saved to {path}")

        print(f"\nPost-processing: run-post {node.pk} {config_path} --report --dos --band")
        sys.exit(node.exit_status or 0)

    # ── Submit to daemon (default) ────────────────────────────────
    from aiida.engine import submit

    node = submit(WorkChain, inputs)
    print(f"Submitted workchain PK = {node.pk}, UUID = {node.uuid}")

    if not args.no_report:
        output_path = _resolve_report_path(cfg, args.output, node.pk)
        script = Path(__file__).resolve()

        cmd = [
            sys.executable, str(script),
            str(config_path),
            "--background-monitor", str(node.pk),
            "-o", str(output_path),
        ]
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        print(f"Background monitor started for node<{node.pk}> → {output_path}")

    print(f"\nPost-processing after completion: run-post {node.pk} {config_path} --all")
    sys.exit(0)


if __name__ == "__main__":
    main()
