"""DOS plotting utilities for AbacusBandBatchWorkChain.

Extracts density-of-states data from batch workflow children and
generates comparison plots grouped by structure prototype.

Typical usage
-------------
.. code-block:: python

    from aiida_batch.utils.dos import plot_dos
    plot_dos(82883, "config.yaml", output_dir="./dos_plots")
"""

from collections import defaultdict
from pathlib import Path
from typing import Optional, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from aiida import orm

# Distinct colors for different pseudopotentials (Tableau color palette)
_PSEUDO_COLORS = [
    "#4E79A7",  # blue
    "#F28E2B",  # orange
    "#E15759",  # red
    "#76B7B2",  # teal
    "#59A14F",  # green
    "#EDC948",  # yellow
    "#B07AA1",  # purple
    "#FF9DA7",  # pink
    "#9C755F",  # brown
    "#BAB0AC",  # gray
]


def _load_config(config_path: Path) -> dict:
    import yaml
    with open(config_path) as f:
        return yaml.safe_load(f)


def _pseudo_label(pseudo: str, config: dict) -> str:
    """Return a human-friendly label for a pseudo family.

    Uses the optional ``plot.pseudo_labels`` mapping in the config.
    """
    labels = (config.get("plot") or {}).get("pseudo_labels", {})
    return labels.get(pseudo, pseudo)


def _pseudo_color(pseudo: str) -> str:
    """Return a colour for a pseudo family.
    
    Uses a consistent color based on a hash of the pseudo name,
    cycling through the predefined color palette.
    """
    color_idx = hash(pseudo) % len(_PSEUDO_COLORS)
    return _PSEUDO_COLORS[color_idx]


# ------------------------------------------------------------------
#  DOS data extraction
# ------------------------------------------------------------------


def get_dos_data(band_node: orm.WorkChainNode):
    """Extract DOS data from a single ``AbacusBandWorkChain`` node.

    Parameters
    ----------
    band_node:
        An ``AbacusBandWorkChain`` node (child of the batch workflow).

    Returns
    -------
    dict with keys ``fermi_energy``, ``energy``, ``tdos``, or
    ``None`` if the data could not be extracted.
    """
    try:
        # The last called child of the band workchain is the DOS calculation.
        dos_child = band_node.called[-1]
        misc = dos_child.outputs.misc.get_dict()
        fermi_energy = misc.get("fermi_level")

        dos_node = dos_child.outputs.dos
        energy = dos_node.get_array("energy")
        tdos = dos_node.get_array("tdos")

        return {
            "fermi_energy": fermi_energy,
            "energy": energy,
            "tdos": tdos,
        }
    except Exception:
        return None


def get_dos_data_from_outputs(band_node: orm.WorkChainNode):
    """Alternative DOS extraction via ``band_node.outputs.dos``.

    Falls back to this when ``get_dos_data`` fails.
    """
    try:
        dos_out = band_node.outputs.dos
        energy = dos_out.get_array("energy")
        tdos = dos_out.get_array("tdos")
        # Try to get fermi_level from misc output of the band node itself
        fermi_energy = None
        try:
            misc = band_node.outputs.misc.get_dict()
            fermi_energy = misc.get("fermi_level")
        except Exception:
            pass
        return {
            "fermi_energy": fermi_energy,
            "energy": energy,
            "tdos": tdos,
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
    """Iterate over a batch workflow's children and collect DOS curves.

    Each returned dict has keys: ``pseudo``, ``proto``, ``label``,
    ``energy_shift`` (eV), ``tdos``, ``color``, ``linestyle``.

    Parameters
    ----------
    batch_pk:
        PK or UUID of the ``AbacusBandBatchWorkChain`` node.
    config:
        Parsed YAML config (for pseudo ordering and labels).

    Returns
    -------
    List of curve dicts.
    """
    from aiida import orm as _orm
    node = _orm.load_node(batch_pk)

    # Get child results from outputs.results or fallback to called
    children = []
    try:
        results_node = node.outputs.results
        if isinstance(results_node, _orm.Dict):
            children = results_node.get_dict().get("children", [])
    except AttributeError:
        pass

    if not children:
        # Fallback: collect from called children
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
            wc_node = _orm.load_node(pk)
        except Exception:
            continue

        dos_data = get_dos_data(wc_node)
        if dos_data is None:
            dos_data = get_dos_data_from_outputs(wc_node)
        if dos_data is None:
            continue

        fermi = dos_data["fermi_energy"]
        energy = dos_data["energy"]
        tdos = dos_data["tdos"]

        if fermi is None:
            continue

        energy_shift = energy - fermi
        label = f"{_pseudo_label(pseudo, config)}"

        curves.append({
            "pseudo": pseudo,
            "proto": proto,
            "label": label,
            "energy_shift": energy_shift,
            "tdos": tdos,
            "color": _pseudo_color(pseudo),
            "linestyle": "-",
        })

    return curves


# ------------------------------------------------------------------
#  Plotting
# ------------------------------------------------------------------


def plot_curves_by_structure(
    curves: list[dict],
    output_dir: Path,
    xlim: tuple[float, float] = (-5, 7),
    protos: Optional[list[str]] = None,
    dpi: int = 150,
    show_fermi: bool = True,
) -> list[Path]:
    """Generate one plot per structure prototype with all pseudos overlaid.

    Parameters
    ----------
    curves:
        List of curve dicts from :func:`collect_curves`.
    output_dir:
        Directory where PNG files are saved.
    xlim:
        Energy range relative to Fermi level (eV).
    protos:
        Subset of prototypes to plot.  ``None`` → all.
    dpi:
        Figure resolution.
    show_fermi:
        Whether to draw a vertical line at E_F.

    Returns
    -------
    List of saved file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Group curves by structure prototype
    groups: dict[str, list[dict]] = defaultdict(list)
    for c in curves:
        groups[c["proto"]].append(c)

    if protos:
        ordered = [p for p in protos if p in groups]
    else:
        ordered = list(groups.keys())

    saved = []
    for proto in ordered:
        group = groups[proto]
        fig, ax = plt.subplots(figsize=(8, 5))

        # Determine y-axis range
        ymax = 0.0
        for c in group:
            mask = (c["energy_shift"] >= xlim[0]) & (c["energy_shift"] <= xlim[1])
            if np.any(mask):
                ymax = max(ymax, np.max(c["tdos"][mask]))
        ylim = (0, ymax + 0.5 * max(1, ymax * 0.1))

        for c in group:
            ax.plot(
                c["energy_shift"], c["tdos"],
                color=c["color"], linestyle=c.get("linestyle", "-"),
                linewidth=1.5, label=c["label"],
            )

        if show_fermi:
            ax.axvline(x=0, color="r", linestyle="--", linewidth=1, label="Fermi level")

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xlabel("Energy – Fermi Level (eV)")
        ax.set_ylabel("DOS")
        ax.set_title(proto)
        ax.legend(fontsize="small")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        path = output_dir / f"dos_{proto}.png"
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        saved.append(path)
        print(f"  Saved: {path} ({len(group)} curves)")

    return saved


def plot_dos(
    batch_pk: Union[int, str],
    config_path: Union[str, Path],
    output_dir: Union[str, Path] = "./dos_plots",
    xlim: tuple[float, float] = (-5, 7),
    dpi: int = 150,
) -> list[Path]:
    """High-level convenience: collect curves and plot.

    Parameters
    ----------
    batch_pk:
        PK or UUID of the ``AbacusBandBatchWorkChain`` node.
    config_path:
        Path to the YAML config file.
    output_dir:
        Output directory for PNG files.
    xlim:
        Energy range relative to Fermi level (eV).
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
        print("No DOS curves collected (maybe the workflow is still running?).")
        return []

    print(f"Collected {len(curves)} DOS curve(s), plotting by structure …")
    return plot_curves_by_structure(curves, Path(output_dir), xlim=xlim, protos=protos, dpi=dpi)


# ── standalone entry point ──────────────────────────────────────────────────


def main():
    """CLI entry point for ``python -m aiida_batch.utils.dos``."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plot DOS curves from an AbacusBandBatchWorkChain result."
    )
    parser.add_argument("pk", type=int, help="PK of the batch workflow node")
    parser.add_argument("config", type=Path, help="Path to YAML config file")
    parser.add_argument(
        "-o", "--output-dir", default="./dos_plots",
        help="Output directory for plots (default: ./dos_plots)",
    )
    parser.add_argument(
        "--xmin", type=float, default=-5.0,
        help="Energy lower bound (eV, default: -5)",
    )
    parser.add_argument(
        "--xmax", type=float, default=7.0,
        help="Energy upper bound (eV, default: 7)",
    )
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="Figure resolution (default: 150)",
    )
    args = parser.parse_args()

    from aiida import load_profile
    load_profile()

    saved = plot_dos(
        args.pk, args.config,
        output_dir=args.output_dir,
        xlim=(args.xmin, args.xmax),
        dpi=args.dpi,
    )
    print(f"Done — {len(saved)} plot(s) saved.")


if __name__ == "__main__":
    main()
