"""Batch-submit ``vasp.v2.bands`` for multiple potentials and structures.

Entry point
-----------
* ``vasp.band.batch`` → ``vasp.v2.bands``
"""

from aiida import orm
from aiida.orm import StructureData
from . import VaspBatchSubmitWorkChain


class VaspBandBatchWorkChain(VaspBatchSubmitWorkChain):
    """Batch-submit ``vasp.v2.bands`` for multiple potentials and structures."""

    _child_workchain_entry_point = "vasp.v2.bands"

    @classmethod
    def define(cls, spec):
        super().define(spec)
        child = cls._get_child_workchain_class()
        spec.expose_inputs(
            child,
            include=[
                "scf",
                "bands",
                "structure",
                "band_settings",
            ],
        )
        spec.input("structure", valid_type=orm.StructureData, required=False)

    # ------------------------------------------------------------------

    def _build_child_inputs(self, potential: str, proto: str, atoms) -> dict:
        child = self._get_child_workchain_class()
        inputs = self.exposed_inputs(child, agglomerate=True)
        stru = StructureData(ase=atoms)
        inputs["structure"] = stru
        label = f"{potential}_{proto}"

        # Set structure in scf namespace
        if "scf" not in inputs:
            inputs["scf"] = {}
        inputs["scf"]["structure"] = stru
        inputs["scf"]["potential_family"] = orm.Str(potential)

        # Set label in scf.calc.metadata.options if exists
        scf = inputs["scf"]
        if "calc" in scf and isinstance(scf["calc"], dict):
            scf["calc"].setdefault("metadata", {}).setdefault("options", {})["label"] = label
        elif "calc" not in scf:
            scf["calc"] = {"metadata": {"options": {"label": label}}}

        return inputs

    # ------------------------------------------------------------------

    @classmethod
    def build_inputs_from_config(cls, cfg: dict) -> dict:
        inputs = super().build_inputs_from_config(cfg)
        inp = cfg.get("inputs", {})

        # ── scf namespace ──
        from aiida.orm import Dict, load_code
        scf_cfg = inp.get("scf", {})
        scf_inputs = {}

        if "code" in scf_cfg:
            code_label = scf_cfg["code"]
            if isinstance(code_label, str):
                scf_inputs["code"] = load_code(code_label)
            else:
                scf_inputs["code"] = code_label

        if "kpoints_spacing" in scf_cfg:
            scf_inputs["kpoints_spacing"] = orm.Float(scf_cfg["kpoints_spacing"])

        if "parameters" in scf_cfg:
            scf_inputs["parameters"] = Dict(dict=scf_cfg["parameters"])

        if "potential_family" in scf_cfg:
            scf_inputs["potential_family"] = orm.Str(scf_cfg["potential_family"])

        if "potential_mapping" in scf_cfg:
            scf_inputs["potential_mapping"] = Dict(dict=scf_cfg["potential_mapping"])

        if "calc" in scf_cfg:
            scf_inputs["calc"] = scf_cfg["calc"]

        if scf_inputs:
            inputs["scf"] = scf_inputs

        # ── band_settings ──
        if "band_settings" in inp:
            inputs["band_settings"] = orm.Dict(dict=inp["band_settings"])

        return inputs
