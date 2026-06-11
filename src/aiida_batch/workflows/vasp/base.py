"""Batch-submit ``vasp.base`` for multiple potentials and structures.

Entry point
-----------
* ``vasp.base.batch``
"""

from aiida import orm
from aiida.orm import StructureData
from . import VaspBatchSubmitWorkChain


class VaspBaseBatchWorkChain(VaspBatchSubmitWorkChain):
    """Batch-submit ``vasp.base`` for multiple potentials and structures."""

    _child_workchain_entry_point = "vasp.base"

    @classmethod
    def define(cls, spec):
        super().define(spec)
        child = cls._get_child_workchain_class()
        spec.expose_inputs(
            child, include=["vasp_structure", "vasp_code", "vasp incar",
                           "vasp_kpoints", "potential_family", "potential_mapping"]
        )
        # structure is generated internally per child
        spec.input("vasp.vasp_structure", valid_type=orm.StructureData, required=False)

    # ------------------------------------------------------------------

    def _build_child_inputs(self, potential: str, proto: str, atoms) -> dict:
        child = self._get_child_workchain_class()
        inputs = self.exposed_inputs(child, agglomerate=True)
        inputs["vasp_structure"] = StructureData(ase=atoms)
        inputs["potential_family"] = orm.Str(potential)
        label = f"{potential}_{proto}"
        inputs.setdefault("metadata", {})
        inputs["metadata"]["label"] = label
        return inputs

    # ------------------------------------------------------------------

    @classmethod
    def build_inputs_from_config(cls, cfg: dict) -> dict:
        inputs = super().build_inputs_from_config(cfg)
        inp = cfg.get("inputs", {})

        # ── vasp namespace ──
        vasp_cfg = inp.get("vasp", {})
        inputs.update(cls._build_vasp_namespace(vasp_cfg))

        if "kpoints_distance" in inp:
            inputs["kpoints_distance"] = orm.Float(inp["kpoints_distance"])

        return inputs
