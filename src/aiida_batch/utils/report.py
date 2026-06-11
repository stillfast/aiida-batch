"""Utility for generating markdown reports from an AbacusBatchSubmitWorkChain.

Public API
----------
- ``generate_report(pk_or_uuid, config_path, output_path)``
    Generate the full report immediately (workflow must have finished).
- ``monitor_and_report(pk_or_uuid, config_path, output_path, poll_interval=60)``
    Poll until the workflow reaches a terminal state, then generate the report.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import yaml
from aiida import orm
from aiida.engine import ProcessState

# ── helpers ──────────────────────────────────────────────────────────────────


def _load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def _collect_from_children(node):
    """Collect child info from called processes when the workflow has no results output."""
    children = []
    for child in node.called:
        pseudo = child.base.extras.get("pseudo_family", None)
        proto = child.base.extras.get("structure_name", None)
        if pseudo is None or proto is None:
            continue
        children.append(
            {
                "pseudo": pseudo,
                "proto": proto,
                "pk": child.pk,
                "exit_status": child.exit_status,
                "ok": child.is_finished_ok,
            }
        )
    return children


def _status_emoji(node):
    if hasattr(node, "is_finished_ok") and node.is_finished_ok:
        return "🟢"
    if hasattr(node, "process_state") and node.process_state and node.process_state.value in ("excepted", "killed"):
        return "🔴"
    return "🟡"


def _status_label(node):
    if hasattr(node, "is_finished_ok") and node.is_finished_ok:
        return f"Finished [{node.exit_status}]"
    if hasattr(node, "process_state") and node.process_state:
        s = node.process_state.value.capitalize()
        es = f" [{node.exit_status}]" if node.exit_status is not None else ""
        return f"{s}{es}"
    return "—"


# ── tree formatting ──────────────────────────────────────────────────────────


def _collect_calc_nodes(node):
    """Recursively collect CalcJobNode instances from *node* and its called children."""
    from aiida.orm import CalcJobNode, WorkChainNode

    results = []
    for child in node.called:
        if isinstance(child, CalcJobNode):
            results.append(child)
        elif isinstance(child, WorkChainNode):
            results.extend(_collect_calc_nodes(child))
    return results


def _format_child_tree(wc_node):
    """Build a code-fence tree showing the sub-process structure of a workchain.

    Uses ``wc_node.called`` to only include sub-processes (workchains and
    calculations), skipping data nodes like StructureData, Dict, etc.

    Returns (tree_text, calc_nodes) where calc_nodes is a list of
    (CalcJobNode, parent_wc_node).  ``parent_wc_node`` is the top-level
    child workchain used for ``child-XXXX`` back-links.
    """
    from aiida.orm import CalcJobNode, WorkChainNode

    child_nodes = list(wc_node.called)
    calc_nodes_out = []

    lines = []
    indent = "    "
    wc_emoji = _status_emoji(wc_node)
    wc_type = getattr(wc_node, "process_label", type(wc_node).__name__)
    lines.append(f"{wc_emoji} {wc_type}<{wc_node.pk}> {_status_label(wc_node)}")

    child_display_lines = []
    for node in child_nodes:
        emoji = _status_emoji(node)
        ntype = getattr(node, "process_label", type(node).__name__)

        if isinstance(node, CalcJobNode):
            link = f"[{ntype}<{node.pk}>](#calc-{node.pk})"
            child_display_lines.append(f"{emoji} {link} {_status_label(node)}")
            calc_nodes_out.append((node, wc_node))
        elif isinstance(node, WorkChainNode):
            child_display_lines.append(f"{emoji} {ntype}<{node.pk}> {_status_label(node)}")
            for calc_child in _collect_calc_nodes(node):
                calc_nodes_out.append((calc_child, wc_node))
        else:
            child_display_lines.append(f"{emoji} {ntype}<{node.pk}> {_status_label(node)}")

    for idx, line in enumerate(child_display_lines):
        prefix = "├── " if idx < len(child_display_lines) - 1 else "└── "
        lines.append(indent + prefix + line)

    return "\n".join(lines), calc_nodes_out


def _format_calc_details(calc_node, parent_wc_node=None):
    """Format details for an AbacusCalculation node.

    Uses ``aiida.cmdline.utils.common.get_calcjob_report`` for log output.
    """
    from aiida.cmdline.utils.common import get_calcjob_report

    attrs = calc_node.base.attributes.all
    job_id = attrs.get("job_id", "—")
    remote_workdir = attrs.get("remote_workdir", "—")

    walltime_str = None
    last = attrs.get("last_job_info", {})
    wall_secs = last.get("wallclock_time_seconds") if isinstance(last, dict) else None
    if wall_secs is not None:
        try:
            secs = int(wall_secs)
            h, remainder = divmod(secs, 3600)
            m, s = divmod(remainder, 60)
            walltime_str = f"{h:02d}:{m:02d}:{s:02d}"
        except (ValueError, TypeError):
            pass

    lines = [f"### calc-{calc_node.pk}  <a id=\"calc-{calc_node.pk}\"></a>", ""]
    lines.append(f"**AbacusCalculation <{calc_node.pk}>**")
    lines.append("")
    lines.append(f"[⬆ Back to child details](#child-{parent_wc_node.pk})")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Scheduler JobID | `{job_id}` |")
    if walltime_str:
        lines.append(f"| Walltime | {walltime_str} |")
    lines.append(f"| Remote Path | `{remote_workdir}` |")
    lines.append("")

    # Use aiida-core's built-in calcjob report (same as `verdi process report`)
    calc_report = get_calcjob_report(calc_node)
    if calc_report:
        lines.append("**Report Logs:**")
        lines.append("")
        lines.append("```")
        lines.append(calc_report)
        lines.append("```")
    else:
        lines.append("_(no report logs)_")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


# ── core API ─────────────────────────────────────────────────────────────────


def generate_report(
    pk_or_uuid: Union[int, str],
    config_path: Path,
    output_path: Path,
) -> str:
    """Generate a full markdown report for an AbacusBatchSubmitWorkChain.

    Parameters
    ----------
    pk_or_uuid:
        PK or UUID of the workflow node.
    config_path:
        Path to the YAML config file (used for proto/pseudo ordering).
    output_path:
        Where to write the report.

    Returns
    -------
    The absolute path of the written report file.
    """
    # ── load config ──
    cfg = _load_config(config_path)
    inp = cfg.get("inputs", cfg)
    protos: list[str] = inp.get("structure_config", {}).get("protos", [])
    if not protos:
        raise ValueError("no 'protos' found in structure_config")

    # ── load workflow node ──
    node = orm.load_node(pk_or_uuid)

    # ── get child results ──
    try:
        results_node = node.outputs.results
        if isinstance(results_node, orm.Dict):
            children = results_node.get_dict().get("children", [])
        else:
            children = []
    except AttributeError:
        children = []

    if not children:
        children = _collect_from_children(node)

    if not children:
        raise ValueError(f"no child data found for node {pk_or_uuid}")

    # ── build exit-code matrix ──
    pseudo_order: list[str] = []
    exit_map: dict[tuple[str, str], dict] = {}
    all_pseudos_set: set[str] = set()

    for child in children:
        pseudo = child["pseudo"]
        proto = child["proto"]
        all_pseudos_set.add(pseudo)
        exit_map[(pseudo, proto)] = child

    col_protos = list(protos)

    seen = set()
    for child in children:
        p = child["pseudo"]
        if p not in seen:
            pseudo_order.append(p)
            seen.add(p)
    for p in sorted(all_pseudos_set):
        if p not in seen:
            pseudo_order.append(p)
            seen.add(p)

    # ── compose report ──
    report_lines = []

    # Title
    report_lines.append("# Batch Workflow Report")
    report_lines.append("")
    pk = node.pk
    wc_type = getattr(node, "process_label", type(node).__name__)
    report_lines.append(f"**Workflow**: {wc_type}<{pk}>")
    report_lines.append(f"**Status**: {_status_label(node)}")
    report_lines.append(f"**Report generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # ── 1. Exit code table ──
    report_lines.append("## 1. Exit Code Summary")
    report_lines.append("")

    header = ["Pseudo"] + col_protos
    separator = ["---"] + [":---:"] * len(col_protos)

    rows_tbl = [header, separator]
    for pseudo in pseudo_order:
        row = [pseudo]
        for proto in col_protos:
            child = exit_map.get((pseudo, proto))
            if child is None:
                row.append("—")
            else:
                pk_child = child["pk"]
                es = child["exit_status"]
                row.append(f"[{es}](#child-{pk_child})")
        rows_tbl.append(row)

    for r in rows_tbl:
        report_lines.append("| " + " | ".join(r) + " |")
    report_lines.append("")
    report_lines.append("[⬇ Jump to child details](#2-child-workflow-details)")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # ── 2. Child workflow details ──
    report_lines.append("## 2. Child Workflow Details")
    report_lines.append("")

    all_calc_nodes = []

    for pseudo in pseudo_order:
        for proto in col_protos:
            child = exit_map.get((pseudo, proto))
            if child is None:
                continue
            pk_child = child["pk"]
            es = child["exit_status"]

            try:
                wc_node = orm.load_node(pk_child)
            except Exception:
                continue

            report_lines.append(f"### child-{pk_child}  <a id=\"child-{pk_child}\"></a>")
            report_lines.append("")
            report_lines.append("[⬆ Back to exit code table](#1-exit-code-summary)")
            report_lines.append("")
            report_lines.append(f"**Pseudo**: `{pseudo}`  |  **Proto**: `{proto}`  |  **Exit**: `{es}`")
            report_lines.append("")

            tree_text, calc_nodes = _format_child_tree(wc_node)
            report_lines.append("```")
            report_lines.append(tree_text)
            report_lines.append("```")
            report_lines.append("")

            for cnode, _ in calc_nodes:
                report_lines.append(f"- [AbacusCalculation<{cnode.pk}> details](#calc-{cnode.pk})")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

            all_calc_nodes.extend(calc_nodes)

    # ── 3. Calculation details ──
    report_lines.append("## 3. Calculation Details")
    report_lines.append("")

    for calc_node, parent_wc_node in all_calc_nodes:
        section = _format_calc_details(calc_node, parent_wc_node)
        report_lines.append(section)

    # ── write ──
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    return str(output_path)


def monitor_and_report(
    pk_or_uuid: Union[int, str],
    config_path: Path,
    output_path: Path,
    poll_interval: int = 60,
    max_poll_time: int | None = None,
    on_progress: Optional[callable] = None,
) -> str:
    """Poll the workflow until it reaches a terminal state, then generate the report.

    Terminal states (from ``ProcessState``): ``FINISHED``, ``EXCEPTED``, ``KILLED``.

    Parameters
    ----------
    pk_or_uuid:
        PK or UUID of the workflow node.
    config_path:
        Path to the YAML config file.
    output_path:
        Where to write the report.
    poll_interval:
        Seconds between each status check (default 60).
    max_poll_time:
        Maximum total wall-clock time in seconds to keep polling.
        When exceeded the report is generated anyway (best-effort).
        ``None`` means poll indefinitely (default).
    on_progress:
        Optional callback ``f(state)`` called after each poll.

    Returns
    -------
    The absolute path of the written report file.
    """
    _TERMINAL_STATES = {ProcessState.FINISHED, ProcessState.EXCEPTED, ProcessState.KILLED}

    node = orm.load_node(pk_or_uuid)
    start_time = time.time()

    while node.process_state not in _TERMINAL_STATES:
        state_label = node.process_state.value if node.process_state else "UNKNOWN"

        if max_poll_time is not None:
            elapsed = time.time() - start_time
            if elapsed >= max_poll_time:
                print(f"[monitor] node<{node.pk}> max_poll_time ({max_poll_time}s) reached, "
                      f"generating report with current state={state_label}...")
                break

        if on_progress:
            on_progress(state_label)
        else:
            print(f"[monitor] node<{node.pk}> state={state_label} — waiting {poll_interval}s...")
        time.sleep(poll_interval)
        node = orm.load_node(node.pk)

    state_label = node.process_state.value if node.process_state else "UNKNOWN"
    if on_progress:
        on_progress(state_label)
    else:
        print(f"[monitor] node<{node.pk}> state={state_label} — terminated, generating report...")

    return generate_report(pk_or_uuid, config_path, output_path)
