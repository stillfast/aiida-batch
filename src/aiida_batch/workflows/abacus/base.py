"""Batch-submit ``abacus.base`` for multiple pseudos and structures.

Entry point
-----------
* ``abacus.base.batch``
"""

from aiida import orm
from aiida.orm import StructureData
from . import AbacusBatchSubmitWorkChain


class AbacusBaseBatchWorkChain(AbacusBatchSubmitWorkChain):
    """Batch-submit ``abacus.base`` for multiple pseudos and structures."""

    _child_workchain_entry_point = "abacus.base"

    @classmethod
    def define(cls, spec):
        super().define(spec)
        child = cls._get_child_workchain_class()
        spec.expose_inputs(
            child, include=["abacus", "kpoints_distance", "pseudo_family"]
        )
        # structure is generated internally per child
        spec.input("abacus.structure", valid_type=orm.StructureData, required=False)

    # ------------------------------------------------------------------

    def _build_child_inputs(self, pseudo: str, proto: str, atoms) -> dict:
        child = self._get_child_workchain_class()
        inputs = self.exposed_inputs(child, agglomerate=True)
        inputs["abacus"]["structure"] = StructureData(ase=atoms)
        inputs["pseudo_family"] = orm.Str(pseudo)
        label = f"{pseudo}_{proto}"
        inputs["abacus"].setdefault("metadata", {})
        inputs["abacus"]["metadata"]["label"] = label
        return inputs

    # ------------------------------------------------------------------

    @classmethod
    def build_inputs_from_config(cls, cfg: dict) -> dict:
        inputs = super().build_inputs_from_config(cfg)
        inp = cfg.get("inputs", {})

        abacus_cfg = inp.get("abacus", {})
        inputs["abacus"] = cls._build_abacus_namespace(abacus_cfg)

        if "kpoints_distance" in inp:
            inputs["kpoints_distance"] = orm.Float(inp["kpoints_distance"])

        if "pseudo_family" in inp:
            inputs["abacus"]["pseudo_family"] = orm.Str(inp["pseudo_family"])

        return inputs
