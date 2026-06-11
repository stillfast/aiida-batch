#!/usr/bin/env python3
"""CLI for inspecting / reporting on an AbacusBatchSubmitWorkChain.

Usage:
    # Quick exit-code table (stdout)
    python batch_inspect.py <pk_or_uuid> <config_path>

    # Full markdown report (saved to file)
    python batch_inspect.py <pk_or_uuid> <config_path> --full-report [-o REPORT.md]

    # Monitor + full report (poll until done, then write report)
    python batch_inspect.py <pk_or_uuid> <config_path> --monitor [-o REPORT.md] [--poll 60]
"""

import argparse
import sys
from pathlib import Path

from aiida import load_profile, orm
from aiida_batch.utils.report import generate_report, monitor_and_report


def main():
    parser = argparse.ArgumentParser(
        description="Inspect / report on an AbacusBatchSubmitWorkChain."
    )
    parser.add_argument("identifier", help="PK or UUID of the workflow node")
    parser.add_argument(
        "config",
        type=Path,
        help="Path to config.yaml",
    )
    parser.add_argument(
        "--full-report",
        action="store_true",
        help="Generate a complete markdown report and save to file",
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Poll the workflow until terminated, then generate the full report",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path (default: batch-report-<pk>.md)",
    )
    parser.add_argument(
        "--poll",
        type=int,
        default=60,
        help="Poll interval in seconds (default: 60)",
    )
    args = parser.parse_args()

    config_path = args.config.resolve()
    if not config_path.exists():
        print(f"Error: config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    load_profile()

    # ── Quick table mode (no --full-report or --monitor) ──
    if not args.full_report and not args.monitor:
        import yaml
        cfg = yaml.safe_load(config_path.read_text())
        inp = cfg.get("inputs", cfg)
        protos = inp.get("structure_config", {}).get("protos", [])
        node = orm.load_node(args.identifier)

        try:
            results_node = node.outputs.results
            children = results_node.get_dict().get("children", []) if isinstance(results_node, orm.Dict) else []
        except AttributeError:
            children = []

        if not children:
            from aiida_batch.utils.report import _collect_from_children
            children = _collect_from_children(node)

        if not children:
            print("Error: no child data found", file=sys.stderr)
            sys.exit(1)

        pseudo_order = []
        exit_map = {}
        seen = set()
        for child in children:
            exit_map[(child["pseudo"], child["proto"])] = child["exit_status"]
            if child["pseudo"] not in seen:
                pseudo_order.append(child["pseudo"])
                seen.add(child["pseudo"])

        header = ["Pseudo"] + list(protos)
        sep = ["---"] + ["---"] * len(protos)
        rows = [header, sep]
        for pseudo in pseudo_order:
            row = [pseudo]
            for proto in protos:
                val = exit_map.get((pseudo, proto), "—")
                row.append(str(val))
            rows.append(row)

        widths = [max(len(str(r[i])) for r in rows) for i in range(len(header))]
        for r in rows:
            print("| " + " | ".join(cell.ljust(w) for cell, w in zip(r, widths)) + " |")
        return

    # ── Full report mode ──
    if args.full_report:
        if args.output is None:
            output_path = Path(f"batch-report-{args.identifier}.md").resolve()
        else:
            output_path = Path(args.output).resolve()
        path = generate_report(args.identifier, config_path, output_path)
        print(f"Report saved to {path}", file=sys.stderr)
        return

    # ── Monitor mode ──
    if args.monitor:
        if args.output is None:
            output_path = Path(f"batch-report-{args.identifier}.md").resolve()
        else:
            output_path = Path(args.output).resolve()
        path = monitor_and_report(args.identifier, config_path, output_path, poll_interval=args.poll)
        print(f"Report saved to {path}", file=sys.stderr)
        return


if __name__ == "__main__":
    main()
