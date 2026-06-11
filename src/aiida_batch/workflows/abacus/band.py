"""Batch-submit ``abacus.band`` for multiple pseudos and structures.

Entry point
-----------
* ``abacus.band.batch``
"""

from aiida import orm
from aiida.orm import StructureData
from . import AbacusBatchSubmitWorkChain


class AbacusBandBatchWorkChain(AbacusBatchSubmitWorkChain):
    """Batch-submit ``abacus.band`` for multiple pseudos and structures."""

    _child_workchain_entry_point = "abacus.band"

    @classmethod
    def define(cls, spec):
        super().define(spec)
        child = cls._get_child_workchain_class()
        spec.expose_inputs(
            child, include=["base", "kpoints_band", "band_settings"]
        )
        # structure is generated internally per child
        spec.input("base.abacus.structure", valid_type=orm.StructureData, required=False)

    # ------------------------------------------------------------------

    def _build_child_inputs(self, pseudo: str, proto: str, atoms) -> dict:
        child = self._get_child_workchain_class()
        inputs = self.exposed_inputs(child, agglomerate=True)
        stru = StructureData(ase=atoms)
        # AbacusBandWorkChain needs the structure in two places:
        #   - top-level (directly required by band)
        #   - base.abacus (for the underlying base workchain)
        inputs["structure"] = stru
        inputs["base"]["abacus"]["structure"] = stru
        inputs["base"]["pseudo_family"] = orm.Str(pseudo)
        label = f"{pseudo}_{proto}"
        inputs["base"]["abacus"].setdefault("metadata", {})
        inputs["base"]["abacus"]["metadata"]["label"] = label
        return inputs

    # ------------------------------------------------------------------

    @classmethod
    def build_inputs_from_config(cls, cfg: dict) -> dict:
        inputs = super().build_inputs_from_config(cfg)
        inp = cfg.get("inputs", {})

        # ── base namespace ──
        base_cfg = inp.get("base", {})
        abacus_cfg = base_cfg.get("abacus", {})
        inputs["base"] = {
            "abacus": cls._build_abacus_namespace(abacus_cfg),
        }

        if "kpoints_distance" in base_cfg:
            inputs["base"]["kpoints_distance"] = orm.Float(base_cfg["kpoints_distance"])

        if "pseudo_family" in base_cfg:
            inputs["base"]["pseudo_family"] = orm.Str(base_cfg["pseudo_family"])

        if "max_iterations" in base_cfg:
            inputs["base"]["max_iterations"] = orm.Int(base_cfg["max_iterations"])

        # ── band-specific ──
        if "band_settings" in inp:
            inputs["band_settings"] = orm.Dict(dict=inp["band_settings"])

        if "kpoints_band" in inp:
            from aiida.orm import KpointsData
            kp = KpointsData()
            kp.set_kpoints_mesh(inp["kpoints_band"])
            inputs["kpoints_band"] = kp

        return inputs
