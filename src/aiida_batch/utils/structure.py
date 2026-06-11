"""
Crystal structure generation utilities.

Core function: :func:`make_structure` generates an :class:`ase.Atoms` from a
prototype name and lattice constant.  The :data:`CONFIG` dictionary uses ``"X"``
as a placeholder for the central element, which can be substituted via the
*element* argument of :func:`make_structure`, :func:`generate_all`, etc.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

import ase
from ase.io import write
from pyxtal import pyxtal

# ── configuration ──────────────────────────────────────────────────────────────
# prototype -> (space_group, wyckoff_letters, species_list)
# "X" is a placeholder — use the element= argument to replace it with an
# actual symbol (e.g. "U", "Pu", "Th" …).
CONFIG: Dict[str, Tuple[int, list[str], list[str]]] = {
    "FCC": (225, ["a"], ["X"]),
    "BCC": (229, ["a"], ["X"]),
    "SC": (221, ["a"], ["X"]),
    "Diamond": (227, ["a"], ["X"]),
    "X2O": (225, ["c", "a"], ["X", "O"]),
    "XO": (225, ["a", "b"], ["X", "O"]),
    "X2O3": (224, ["b", "d"], ["X", "O"]),
    "XO2": (225, ["a", "c"], ["X", "O"]),
    "X2O5": (224, ["b", "c", "d"], ["X", "O", "O"]),
    "XO3": (221, ["a", "d"], ["X", "O"]),
}

# Fixed-parameter structures that use a full 1D representation
# (lattice params + free coordinates) instead of a single cubic lattice constant.
#   proto -> (space_group, wyckoff_letters, species_list, x_1d_rep)
FIXED_1D_REP: Dict[str, Tuple[int, list[str], list[str], list[float]]] = {
    # Alpha-U: orthorhombic Cmcm, Wyckoff 4c with y=0.10187
    # x = [a, b, c, y]
    "Alpha-U": (63, ["4c"], ["U"], [2.8364, 5.8666, 4.9363, 0.10187]),
    "Alpha-U-test": (63, ["4c"], ["U"], [2.8420000076, 5.8656997681, 4.9340000153, 0.105]),
}

# Prototypes that are pure-element (unary); everything else is an oxide.
_UNARY_PROTOS: set[str] = {"FCC", "BCC", "SC", "Diamond", "Alpha-U", "Alpha-U-test"}


def _build_json_key_to_proto(element: str) -> Dict[str, str]:
    """Build ``{json_key: prototype_name}`` mapping from :data:`CONFIG`.

    JSON key patterns (see JSON files in ``AE_EOS/``)::

        {element}-X/{proto}   for unaries   (e.g. U-X/BCC)
        {element}-{proto}     for oxides    (e.g. U-X2O)
    """
    mapping: Dict[str, str] = {}
    for proto in CONFIG:
        if proto in _UNARY_PROTOS:
            mapping[f"{element}-X/{proto}"] = proto
        else:
            mapping[f"{element}-{proto}"] = proto
    return mapping


# Paths relative to this file
_HERE = Path(__file__).parent.resolve()
_STATIC = _HERE / ".." / "static"
_JSON_DIR = _STATIC / "AE_EOS"
_STRUCTURES_DIR = _STATIC / "structures"

_DEFAULT_A = 5.0  # default lattice constant (Å) for first-pass generation


# ── helpers ────────────────────────────────────────────────────────────────────


def _cube_root(v: float) -> float:
    return v ** (1.0 / 3.0)


def _resolve_config(element: str) -> Dict[str, Tuple[int, list[str], list[str]]]:
    """Return a copy of :data:`CONFIG` with ``"X"`` replaced by *element*."""
    resolved: Dict[str, Tuple[int, list[str], list[str]]] = {}
    for proto, (spg, wps, species) in CONFIG.items():
        resolved[proto] = (spg, wps, [s.replace("X", element) for s in species])
    return resolved


def _to_primitive(atoms: ase.Atoms, symprec: float = 1e-5) -> Optional[ase.Atoms]:
    """Convert a conventional cell to a primitive cell via spglib.

    Parameters
    ----------
    atoms:
        Input ASE structure.
    symprec:
        Symmetry-finding tolerance.  Default 1e-5.

    Returns
    -------
    ase.Atoms or None
        Primitive cell, or *None* if spglib could not determine it.
    """
    import spglib

    cell = (atoms.get_cell(), atoms.get_scaled_positions(), atoms.get_atomic_numbers())
    res = spglib.find_primitive(cell, symprec=symprec)
    if res is None:
        return None
    p_lattice, p_positions, p_numbers = res
    return ase.Atoms(cell=p_lattice, scaled_positions=p_positions, numbers=p_numbers, pbc=True)


# ── core generation ────────────────────────────────────────────────────────────


def make_structure(proto: str, a: float = _DEFAULT_A, element: str = "U") -> ase.Atoms:
    """Generate a *cubic* crystal structure by prototype name and lattice constant.

    Parameters
    ----------
    proto:
        Prototype name, e.g. ``"FCC"``, ``"XO2"`` (case-insensitive).
    a:
        Lattice constant in Å.  Default 5.0 Å.
    element:
        Element symbol to substitute for ``"X"`` in :data:`CONFIG`.
        Default ``"U"``.

    Returns
    -------
    ase.Atoms

    Raises
    ------
    KeyError
        Unknown prototype.
    RuntimeError
        :mod:`pyxtal` failed to build the structure.
    """
    key = proto
    cfg = _resolve_config(element)
    if key not in cfg:
        raise KeyError(f"Unknown prototype: {proto!r}.  Available: {list(CONFIG)}")

    spg, wps, species = cfg[key]
    try:
        cry = pyxtal()
        cry.from_spg_wps_rep(spg, wps, [a], species)
        return cry.to_ase()
    except Exception as exc:
        raise RuntimeError(f"Failed to generate {proto} (a={a}): {exc}")


def make_structure_by_1d_rep(proto: str, x: list[float], element: str = "U") -> ase.Atoms:
    """Generate a crystal structure from a full 1D representation.

    The 1D representation ``x`` bundles lattice parameters and free
    coordinates in the order expected by :meth:`pyxtal.from_spg_wps_rep`.

    Parameters
    ----------
    proto:
        Prototype name (must be in :data:`FIXED_1D_REP`).
    x:
        1D representation, e.g. ``[a, b, c, y]`` for orthorhombic *Cmcm*.
    element:
        Element symbol (default ``"U"``).

    Returns
    -------
    ase.Atoms
    """
    if proto not in FIXED_1D_REP:
        raise KeyError(
            f"Unknown fixed-1D-rep prototype: {proto!r}.  "
            f"Available: {list(FIXED_1D_REP)}"
        )

    spg, wps, species, _ = FIXED_1D_REP[proto]
    species_resolved = [s.replace("X", element) for s in species]
    try:
        cry = pyxtal()
        cry.from_spg_wps_rep(spg, wps, x, species_resolved)
        return cry.to_ase()
    except Exception as exc:
        raise RuntimeError(f"Failed to generate {proto} (x={x}): {exc}")


def _generate_from_volume(
    proto: str,
    total_volume: float,
    total_atoms: int,
    element: str = "U",
) -> ase.Atoms:
    """Generate a structure whose cell volume is scaled to match the
    per-atom volume from a BM-fit result.

    Uses a two-pass approach:
    1. Generate once with ``a = _DEFAULT_A`` to learn the number of atoms
       that pyxtal produces for this prototype.
    2. Scale the lattice constant so that ``V = avg_atom_volume * n_atoms``.
    """
    avg_atom_vol = total_volume / total_atoms
    atoms = make_structure(proto, a=_DEFAULT_A, element=element)
    n_atoms = len(atoms)
    new_a = _cube_root(avg_atom_vol * n_atoms)
    return make_structure(proto, a=new_a, element=element)


# ── JSON loading ───────────────────────────────────────────────────────────────


def load_volumes(element: str = "U") -> Dict[str, Tuple[float, int]]:
    """Read *element* entries from the two AE JSON files.

    Returns ``{json_key: (min_volume, num_atoms_in_sim_cell)}``.

    JSON keys are e.g. ``"U-X/BCC"``, ``"U-X2O"`` (with *element* substituted
    for ``"U"``).
    """
    prefix = f"{element}-"
    result: Dict[str, Tuple[float, int]] = {}

    for fname in (
        _JSON_DIR / "results-unaries-verification-PBE-v1-AE-average.json",
        _JSON_DIR / "results-oxides-verification-PBE-v1-AE-average.json",
    ):
        data = json.loads(fname.read_text(encoding="utf-8"))
        bm_fit = data.get("BM_fit_data", {})
        natoms_map = data.get("num_atoms_in_sim_cell", {})

        for k, v in bm_fit.items():
            if k.startswith(prefix) and isinstance(v, dict) and "min_volume" in v:
                vol = float(v["min_volume"])
                nn = int(natoms_map.get(k, 0))
                if nn > 0:
                    result[k] = (vol, nn)

    return result


# ── high-level API ─────────────────────────────────────────────────────────────


def generate_all(
    element: str = "U",
    protos: Optional[list[str]] = None,
) -> Dict[str, ase.Atoms]:
    """Generate volume-scaled structures for *element* from JSON.

    Parameters
    ----------
    element:
        Element symbol.  Default ``"U"``.
    protos:
        If given, only generate these prototypes (e.g. ``["BCC", "FCC"]``).
        If *None* (default), generate all that have a JSON key.

    Returns
    -------
    dict
        ``{prototype_name: ase.Atoms}``.
    """
    volumes = load_volumes(element)
    structures: Dict[str, ase.Atoms] = {}

    json_to_proto = _build_json_key_to_proto(element)

    print(f"Generating volume-scaled structures for element = {element!r}\n")

    for json_key, (vol, nat) in volumes.items():
        if json_key not in json_to_proto:
            continue
        proto = json_to_proto[json_key]
        if protos is not None and proto not in protos:
            continue
        try:
            atoms = _generate_from_volume(proto, vol, nat, element=element)
            structures[proto] = atoms
            print(
                f"  {json_key:20s} -> {proto:8s}:"
                f"  V = {atoms.get_volume():.4f} Å³  natoms = {len(atoms)}"
            )
        except Exception as e:
            print(f"  WARNING: Failed {json_key}: {e}")

    return structures


def generate_fixed(
    element: str = "U",
    protos: Optional[list[str]] = None,
) -> Dict[str, ase.Atoms]:
    """Generate fixed-1D-rep structures (not from JSON).

    Parameters
    ----------
    element:
        Element symbol.  Default ``"U"``.
    protos:
        If given, only generate these prototypes (e.g. ``["Alpha-U"]``).
        If *None* (default), generate all fixed-parameter prototypes.

    Returns
    -------
    dict
        ``{prototype_name: ase.Atoms}``.
    """
    structures: Dict[str, ase.Atoms] = {}

    print(f"\nGenerating fixed-parameter structures for element = {element!r}\n")

    for proto, (spg, wps, species, x) in FIXED_1D_REP.items():
        if protos is not None and proto not in protos:
            continue
        try:
            atoms = make_structure_by_1d_rep(proto, x, element=element)
            structures[proto] = atoms
            print(
                f"  {proto:12s}: V = {atoms.get_volume():.4f} Å³  "
                f"natoms = {len(atoms)}"
            )
        except Exception as e:
            print(f"  WARNING: Failed {proto}: {e}")

    return structures


def generate_by_protos(
    protos: list[str],
    element: str = "U",
    to_primitive: bool = False,
    symprec: float = 1e-5,
) -> Dict[str, ase.Atoms]:
    """Generate specific prototypes by name, handling both volume-scaled
    (from JSON) and fixed-parameter structures automatically.

    Parameters
    ----------
    protos:
        Prototype names to generate, e.g. ``["BCC", "Alpha-U", "XO2"]``.
    element:
        Element symbol.  Default ``"U"``.
    to_primitive:
        Whether to convert to primitive cell via spglib.
    symprec:
        Symmetry tolerance for primitive-cell detection.

    Returns
    -------
    dict
        ``{prototype_name: ase.Atoms}``.
    """
    structures: Dict[str, ase.Atoms] = {}

    # Split into volume-scaled (in CONFIG) and fixed-parameter
    vol_protos = [p for p in protos if p in CONFIG]
    fixed_protos = [p for p in protos if p in FIXED_1D_REP]

    for p in protos:
        if p not in CONFIG and p not in FIXED_1D_REP:
            print(f"  WARNING: Unknown prototype {p!r}, skipping")

    if vol_protos:
        structures.update(generate_all(element=element, protos=vol_protos))
    if fixed_protos:
        structures.update(generate_fixed(element=element, protos=fixed_protos))

    if to_primitive:
        print("\nConverting to primitive cells ...")
        for proto in list(structures):
            prim = _to_primitive(structures[proto], symprec=symprec)
            if prim is not None:
                print(
                    f"  {proto:12s}: {len(structures[proto])} -> {len(prim)} atoms"
                )
                structures[proto] = prim
            else:
                print(f"  WARNING: Could not find primitive cell for {proto}")

    return structures


# ── CLI ────────────────────────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate crystal structures for uranium-potential testing."
    )
    parser.add_argument(
        "--protos",
        type=str,
        nargs="+",
        default=None,
        help="Prototype(s) to generate, e.g. BCC XO2 Alpha-U.  Default: all.",
    )
    parser.add_argument(
        "--primitive",
        action="store_true",
        help="Convert to primitive cell via spglib.",
    )
    parser.add_argument(
        "--element",
        type=str,
        default="U",
        help="Element symbol (default: U).",
    )
    args = parser.parse_args()

    element = args.element

    print(f"JSON directory:  {_JSON_DIR}")
    print(f"Output directory: {_STRUCTURES_DIR}\n")

    if args.protos is not None:
        structures = generate_by_protos(
            args.protos, element=element, to_primitive=args.primitive
        )
    else:
        structures = generate_all(element=element)
        structures.update(generate_fixed(element=element))
        if args.primitive:
            print("\nConverting to primitive cells ...")
            for proto in list(structures):
                prim = _to_primitive(structures[proto])
                if prim is not None:
                    print(
                        f"  {proto:12s}: {len(structures[proto])} -> {len(prim)} atoms"
                    )
                    structures[proto] = prim
                else:
                    print(f"  WARNING: Could not find primitive cell for {proto}")

    # Write
    print()
    for proto, atoms in structures.items():
        subdir = "unaries" if proto in _UNARY_PROTOS else "oxides"
        out = _STRUCTURES_DIR / subdir
        out.mkdir(parents=True, exist_ok=True)
        suffix = "_primitive" if args.primitive else ""
        fname = f"{element}-{proto}{suffix}.cif"
        path = out / fname
        write(path, atoms)
        print(f"  {subdir:8s} / {fname}")

    print(f"\nDone — {len(structures)} structure(s) written to {_STRUCTURES_DIR}")


if __name__ == "__main__":
    main()
