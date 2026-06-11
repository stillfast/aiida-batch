#!/usr/bin/env python3
"""Post-processing CLI for batch workflow results.

Generate reports and/or plots from a finished batch workflow node.

Usage
-----
.. code-block:: bash

    run-post <PK> config.yaml --report          # generate report
    run-post <PK> config.yaml --dos             # plot DOS curves
    run-post <PK> config.yaml --band            # plot band structures
    run-post <PK> config.yaml --all             # report + dos + band
    run-post <PK> config.yaml --report --dos -o ./my-report.md   # custom output
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


def load_config(path: Path) -> dict:
    """Load a YAML or JSON config file."""
    import yaml
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    elif path.suffix == ".json":
        import json
        return json.loads(text)
    else:
        raise ValueError(f"Unsupported config file format: {path.suffix}")


def _load_profile(cfg: dict) -> None:
    """Load the AiiDA profile from the config."""
    from aiida import load_profile
    profile_name = cfg.get("profile")
    load_profile(profile_name) if profile_name else load_profile()


def main():
    parser = argparse.ArgumentParser(
        description="Post-process a finished batch workflow.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  run-post 82883 config.yaml --report          generate report\n"
            "  run-post 82883 config.yaml --dos --band       DOS + band plots\n"
            "  run-post 82883 config.yaml --all              everything"
        ),
    )
    parser.add_argument("pk", type=int, help="PK of the batch workflow node")
    parser.add_argument("config", type=Path, help="Path to YAML/JSON config file")
    parser.add_argument(
        "--report", action="store_true",
        help="Generate markdown report",
    )
    parser.add_argument(
        "--dos", action="store_true",
        help="Plot DOS curves",
    )
    parser.add_argument(
        "--band", action="store_true",
        help="Plot band structures",
    )
    parser.add_argument(
        "--all", dest="all", action="store_true",
        help="Generate report + DOS + band plots",
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output path for the report (default: from config or REPORT-<PK>.md)",
    )
    args = parser.parse_args()

    if not any([args.report, args.dos, args.band, args.all]):
        parser.print_help()
        print("\nError: specify at least one of --report, --dos, --band, or --all", file=sys.stderr)
        sys.exit(1)

    config_path = args.config.resolve()
    cfg = load_config(config_path)
    _load_profile(cfg)

    do_report = args.report or args.all
    do_dos = args.dos or args.all
    do_band = args.band or args.all

    # ── Report ──
    if do_report:
        from aiida_batch.utils.report import generate_report
        report_cfg = cfg.get("report", {}) or {}
        out_dir = report_cfg.get("output_dir", ".")
        out_name = report_cfg.get("output_name", "REPORT")
        stem, ext = _parse_name_and_ext(out_name)
        if args.output:
            output_path = Path(args.output).resolve()
        elif out_dir:
            output_path = (Path(out_dir) / f"{stem}-{args.pk}{ext}").resolve()
        else:
            output_path = Path(f"{stem}-{args.pk}{ext}").resolve()

        path = generate_report(args.pk, config_path, output_path)
        print(f"Report saved to {path}")

    # ── DOS plots ──
    if do_dos:
        from aiida_batch.utils.dos import plot_dos
        plot_cfg = cfg.get("plot", {})
        plot_output = plot_cfg.get("dos_output_dir", "./dos_plots")
        xlim = (plot_cfg.get("xmin", -5), plot_cfg.get("xmax", 7))
        dpi = plot_cfg.get("dpi", 150)
        saved = plot_dos(args.pk, config_path, output_dir=plot_output, xlim=xlim, dpi=dpi)
        print(f"DOS plot(s) saved to {plot_output} ({len(saved)} file(s))")

    # ── Band plots ──
    if do_band:
        from aiida_batch.utils.band import plot_band
        band_cfg = cfg.get("plot", {})
        band_output = band_cfg.get("band_output_dir", "./band_plots")
        ymin = band_cfg.get("ymin")
        ymax = band_cfg.get("ymax")
        ylim = (ymin, ymax) if ymin is not None and ymax is not None else None
        dpi = band_cfg.get("dpi", 150)
        saved = plot_band(args.pk, config_path, output_dir=band_output, ylim=ylim, dpi=dpi)
        print(f"Band plot(s) saved to {band_output} ({len(saved)} file(s))")


def _parse_name_and_ext(name: str):
    p = Path(name)
    if p.suffix in (".md", ".markdown", ".html", ".json", ".txt"):
        return p.stem, p.suffix
    return name, ".md"


if __name__ == "__main__":
    main()
