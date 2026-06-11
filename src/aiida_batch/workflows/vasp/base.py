"""Batch-submit ``vasp.v2.vasp`` for multiple potentials and structures.

Entry point
-----------
* ``vasp.base.batch`` → ``vasp.v2.vasp``
"""

from aiida import orm
from aiida.orm import StructureData
from . import VaspBatchSubmitWorkChain


class VaspBaseBatchWorkChain(VaspBatchSubmitWorkChain):
    """Batch-submit ``vasp.v2.vasp`` for multiple potentials and structures."""

    _child_workchain_entry_point = "vasp.v2.vasp"

    @classmethod
    def define(cls, spec):
        super().define(spec)
        child = cls._get_child_workchain_class()
        spec.expose_inputs(
            child,
            include=[
                "code",
                "structure",
                "kpoints",
                "parameters",
                "potential_family",
                "potential_mapping",
                "options",
            ],
        )
        spec.input("structure", valid_type=orm.StructureData, required=False)

    # ------------------------------------------------------------------

    def _build_child_inputs(self, potential: str, proto: str, atoms) -> dict:
        child = self._get_child_workchain_class()
        inputs = self.exposed_inputs(child, agglomerate=True)
        inputs["structure"] = StructureData(ase=atoms)
        inputs["potential_family"] = orm.Str(potential)
        label = f"{potential}_{proto}"
        if "options" not in inputs:
            inputs["options"] = orm.Dict(dict={})
        options = inputs["options"].get_dict()
        options.setdefault("metadata", {})["label"] = label
        inputs["options"] = orm.Dict(dict=options)
        return inputs

    # ------------------------------------------------------------------

    @classmethod
    def build_inputs_from_config(cls, cfg: dict) -> dict:
        inputs = super().build_inputs_from_config(cfg)
        inp = cfg.get("inputs", {})

        # ── vasp namespace ──
        vasp_cfg = inp.get("vasp", {})
        inputs.update(cls._build_vasp_namespace(vasp_cfg))

        if "kpoints_spacing" in inp:
            inputs["kpoints_spacing"] = orm.Float(inp["kpoints_spacing"])

        if "options" in inp:
            inputs["options"] = orm.Dict(dict=inp["options"])

        return inputs
