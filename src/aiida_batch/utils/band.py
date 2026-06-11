"""Band-structure plotting utilities for AbacusBandBatchWorkChain.

Extracts band data from batch workflow children and generates comparison
plots grouped by structure prototype, with all pseudos overlaid.

Typical usage
-------------
.. code-block:: python

    from aiida_batch.utils.band import plot_band
    plot_band(82883, "config.yaml", output_dir="./band_plots")
"""

from collections import defaultdict
from pathlib import Path
from typing import Optional, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from aiida import orm

FALLBACK_COLOR = "#333333"


def _load_config(config_path: Path) -> dict:
    import yaml
    with open(config_path) as f:
        return yaml.safe_load(f)


def _pseudo_label(pseudo: str, config: dict) -> str:
    labels = (config.get("plot") or {}).get("pseudo_labels", {})
    return labels.get(pseudo, pseudo)


def _pseudo_color(pseudo: str) -> str:
    """Return a colour for a pseudo family."""
    return FALLBACK_COLOR


# ------------------------------------------------------------------
#  Band data extraction
# ------------------------------------------------------------------


def get_band_data(band_node: orm.WorkChainNode):
    """Extract band structure from a single ``AbacusBandWorkChain`` node.

    Returns a dict with keys ``fermi_level``, ``bands``, ``labels``,
    ``label_numbers``, or ``None`` if extraction fails.
    """
    try:
        bs = band_node.outputs.band_structure
        fermi_level = bs.base.attributes.get("fermi_level")

        # bands shape: (nspins, nkpoints, nbands) → take spin=0
        bands = bs.get_array("bands")
        if bands.ndim == 3:
            bands = bands[0]  # (nkpoints, nbands)

        labels = bs.base.attributes.get("labels")
        label_numbers = bs.base.attributes.get("label_numbers")

        return {
            "fermi_level": fermi_level,
            "bands": bands,
            "labels": labels,
            "label_numbers": label_numbers,
        }
    except Exception:
        return None


# ------------------------------------------------------------------
#  Collect curves from the batch workflow
# ------------------------------------------------------------------


def collect_curves(
    batch_pk: Union[int, str],
    config: dict,
) -> list[dict]:
    """Iterate over a batch workflow's children and collect band curves.

    Each returned dict has keys: ``pseudo``, ``proto``, ``label``,
    ``fermi_level``, ``bands``, ``labels``, ``label_numbers``,
    ``color``, ``linestyle``, ``linewidth``.
    """
    node = orm.load_node(batch_pk)

    # Get child results from outputs.results or fallback to called children
    children = []
    try:
        results_node = node.outputs.results
        if isinstance(results_node, orm.Dict):
            children = results_node.get_dict().get("children", [])
    except AttributeError:
        pass

    if not children:
        for child in node.called:
            pseudo = child.base.extras.get("pseudo_family", None)
            proto = child.base.extras.get("structure_name", None)
            if pseudo is not None and proto is not None:
                children.append({
                    "pseudo": pseudo,
                    "proto": proto,
                    "pk": child.pk,
                })

    curves = []
    for child in children:
        pseudo = child["pseudo"]
        proto = child["proto"]
        pk = child["pk"]

        try:
            wc_node = orm.load_node(pk)
        except Exception:
            continue

        data = get_band_data(wc_node)
        if data is None:
            continue

        label = f"{_pseudo_label(pseudo, config)} / {proto}"

        curves.append({
            "pseudo": pseudo,
            "proto": proto,
            "label": label,
            "fermi_level": data["fermi_level"],
            "bands": data["bands"],
            "labels": data.get("labels"),
            "label_numbers": data.get("label_numbers"),
            "color": _pseudo_color(pseudo),
            "linestyle": "-",
            "linewidth": 1.0,
        })

    return curves


# ------------------------------------------------------------------
#  Plotting
# ------------------------------------------------------------------


def plot_bands_on_ax(ax, bands_list, ylim=None):
    """Plot multiple band structures on a single ``Axes``.

    Parameters
    ----------
    ax:
        Matplotlib ``Axes``.
    bands_list:
        List of dicts from :func:`collect_curves`.
    ylim:
        ``(ymin, ymax)`` or ``None`` for auto-scaling (2–98 percentile).
    """
    all_energy_shift = []

    for bc in bands_list:
        bands = bc["bands"]
        fermi_level = bc["fermi_level"]
        nkpts = bands.shape[0]

        energy_shift = bands - fermi_level
        all_energy_shift.append(energy_shift)

        for ib in range(bands.shape[1]):
            ax.plot(
                range(nkpts), energy_shift[:, ib],
                color=bc["color"], linestyle=bc.get("linestyle", "-"),
                linewidth=bc.get("linewidth", 1.0),
                alpha=0.8,
            )

    # Fermi level line
    ax.axhline(y=0, color="r", linestyle="--", linewidth=1, alpha=0.7, label="Fermi level")

    # High-symmetry labels
    if bands_list:
        labels = bands_list[0].get("labels", [])
        label_numbers = bands_list[0].get("label_numbers", [])
        nkpts = bands_list[0]["bands"].shape[0]

        if labels and label_numbers:
            ax.set_xticks(label_numbers)
            ax.set_xticklabels(labels)
            for x in label_numbers[1:-1]:
                ax.axvline(x=x, color="gray", linestyle=":", linewidth=0.5, alpha=0.5)
        else:
            ax.set_xlabel("k-points")

        ax.set_xlim(0, nkpts - 1)

    # Y-limits
    if ylim:
        ax.set_ylim(*ylim)
    elif all_energy_shift:
        all_shift = np.concatenate([e.ravel() for e in all_energy_shift])
        p5, p95 = np.percentile(all_shift, [2, 98])
        margin = max(abs(p95 - p5) * 0.1, 2.0)
        ax.set_ylim(p5 - margin, p95 + margin)

    ax.set_ylabel("E - E$_F$ (eV)")
    ax.grid(True, alpha=0.3)


def plot_curves_by_structure(
    curves: list[dict],
    output_dir: Path,
    protos: Optional[list[str]] = None,
    ylim: Optional[tuple[float, float]] = None,
    dpi: int = 150,
    show_fermi: bool = True,
) -> list[Path]:
    """Generate one band-structure plot per structure prototype.

    All pseudos for a given structure are overlaid in a single panel.

    Parameters
    ----------
    curves:
        List of curve dicts from :func:`collect_curves`.
    output_dir:
        Directory where PNG files are saved.
    protos:
        Subset of prototypes to plot.  ``None`` → all.
    ylim:
        ``(ymin, ymax)`` energy window relative to E_F.
    dpi:
        Figure resolution.
    show_fermi:
        Whether to draw a horizontal line at E_F.

    Returns
    -------
    List of saved file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    groups: dict[str, list[dict]] = defaultdict(list)
    for c in curves:
        groups[c["proto"]].append(c)

    if protos:
        ordered = [p for p in protos if p in groups]
    else:
        ordered = list(groups.keys())

    from matplotlib.lines import Line2D

    saved = []
    for proto in ordered:
        group = groups[proto]
        fig, ax = plt.subplots(figsize=(8, 6))

        plot_bands_on_ax(ax, group, ylim=ylim)

        # Legend: one entry per pseudo + fermi level
        handles = [
            Line2D([0], [0], color=c["color"], lw=2, label=c["label"])
            for c in group
        ]
        if show_fermi:
            handles.append(
                Line2D([0], [0], color="r", linestyle="--", lw=1, label="Fermi level")
            )
        ax.legend(handles=handles, fontsize="small")

        ax.set_title(proto)
        fig.tight_layout()

        path = output_dir / f"band_{proto}.png"
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        saved.append(path)
        print(f"  Saved: {path} ({len(group)} curves)")

    return saved


def plot_band(
    batch_pk: Union[int, str],
    config_path: Union[str, Path],
    output_dir: Union[str, Path] = "./band_plots",
    ylim: Optional[tuple[float, float]] = None,
    dpi: int = 150,
) -> list[Path]:
    """High-level convenience: collect curves and plot band structure.

    Parameters
    ----------
    batch_pk:
        PK or UUID of the ``AbacusBandBatchWorkChain`` node.
    config_path:
        Path to the YAML config file.
    output_dir:
        Output directory for PNG files.
    ylim:
        Energy window ``(ymin, ymax)`` relative to E_F.
    dpi:
        Figure resolution.

    Returns
    -------
    List of saved file paths.
    """
    config = _load_config(Path(config_path))
    protos = (
        config.get("inputs", {})
        .get("structure_config", {})
        .get("protos", None)
    )
    curves = collect_curves(batch_pk, config)
    if not curves:
        print("No band curves collected (maybe the workflow is still running?).")
        return []

    print(f"Collected {len(curves)} band curve(s), plotting by structure …")
    return plot_curves_by_structure(curves, Path(output_dir), protos=protos, ylim=ylim, dpi=dpi)


# ── standalone entry point ──────────────────────────────────────────────────


def main():
    """CLI entry point for ``python -m aiida_batch.utils.band``."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plot band structures from an AbacusBandBatchWorkChain result."
    )
    parser.add_argument("pk", type=int, help="PK of the batch workflow node")
    parser.add_argument("config", type=Path, help="Path to YAML config file")
    parser.add_argument(
        "-o", "--output-dir", default="./band_plots",
        help="Output directory for plots (default: ./band_plots)",
    )
    parser.add_argument(
        "--ymin", type=float, default=None,
        help="Energy lower bound (eV, default: auto)",
    )
    parser.add_argument(
        "--ymax", type=float, default=None,
        help="Energy upper bound (eV, default: auto)",
    )
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="Figure resolution (default: 150)",
    )
    args = parser.parse_args()

    from aiida import load_profile
    load_profile()

    ylim = (args.ymin, args.ymax) if args.ymin is not None and args.ymax is not None else None
    saved = plot_band(
        args.pk, args.config,
        output_dir=args.output_dir,
        ylim=ylim,
        dpi=args.dpi,
    )
    print(f"Done — {len(saved)} plot(s) saved.")


if __name__ == "__main__":
    main()
