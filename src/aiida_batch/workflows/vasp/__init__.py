"""Batch-submit VASP calculations for multiple potentials and structures.

Sub-modules
-----------
* :mod:`~aiida_batch.workflows.vasp.base` — child = ``vasp.base``
* :mod:`~aiida_batch.workflows.vasp.band` — child = ``vasp.band``

Entry points
------------
* ``vasp.base.batch`` — batch submit VASP base (scf) calculations
* ``vasp.band.batch`` — batch submit VASP band calculations

Exit codes
----------
    0 : All children finished successfully.
  301 : Some children failed (partial success).
  302 : All children failed.
  401 : Invalid *structure_config* (missing ``protos`` key).
  402 : *potentials_list* is empty or only contains empty strings.
  403 : *structure_config.protos* contains unknown prototypes.
"""

from aiida.engine import WorkChain, ExitCode, append_
from aiida import orm
from aiida.plugins import WorkflowFactory
from aiida.orm import StructureData


# ===========================================================================
#  Base class — shared batch logic for VASP
# ===========================================================================


class VaspBatchSubmitWorkChain(WorkChain):
    """Base batch-submit workchain for VASP.

    Subclasses **must** set ``_child_workchain_entry_point`` (an AiiDA workflow
    entry point string) and override :meth:`_build_child_inputs` to construct
    the per-child input dictionary.

    In ``define()`` subclasses **must** call ``super().define(spec)`` first
    and then ``spec.expose_inputs(child, ...)`` with the child workchain.
    """

    _child_workchain_entry_point: str | None = None

    # ------------------------------------------------------------------
    # class / instance helpers
    # ------------------------------------------------------------------

    @classmethod
    def _get_child_workchain_class(cls):
        """Return the child workchain class from the entry point string."""
        return WorkflowFactory(cls._child_workchain_entry_point)

    # ------------------------------------------------------------------
    # define
    # ------------------------------------------------------------------

    @classmethod
    def define(cls, spec):
        super().define(spec)

        # ── batch-specific inputs (common to all subclasses) ──
        spec.input(
            "structure_config",
            valid_type=orm.Dict,
            help="Dict with keys: protos, element, to_primitive, symprec",
        )
        spec.input(
            "potentials_list",
            valid_type=orm.List,
            help="List of potential family labels (strings).",
        )
        spec.input(
            "potentials_max",
            valid_type=orm.Int,
            required=False,
            default=lambda: orm.Int(99999),
            help="Max number of potential families to use.",
        )
        spec.input(
            "structure_max",
            valid_type=orm.Int,
            required=False,
            default=lambda: orm.Int(99999),
            help="Max number of structures to use per potential family.",
        )
        spec.input(
            "dry_run",
            valid_type=orm.Bool,
            required=False,
            default=lambda: orm.Bool(False),
            help="If True, only print what would be submitted.",
        )

        spec.outline(
            cls.validate_inputs,
            cls.submit_children,
            cls.gather_results,
        )

        spec.output("results", valid_type=orm.Dict)

        # -- exit codes --
        spec.exit_code(
            401,
            "ERROR_INVALID_STRUCTURE_CONFIG",
            message="structure_config missing required key 'protos'",
        )
        spec.exit_code(
            402,
            "ERROR_EMPTY_POTENTIALS_LIST",
            message="potentials_list is empty or contains only blank entries",
        )
        spec.exit_code(
            403,
            "ERROR_INVALID_PROTOS",
            message="structure_config.protos contains unknown prototype names",
        )
        spec.exit_code(
            301,
            "WARNING_PARTIAL_FAILURE",
            message="Some children finished with non-zero exit status",
        )
        spec.exit_code(
            302,
            "ERROR_ALL_FAILED",
            message="All children finished with non-zero exit status",
        )

    # ------------------------------------------------------------------
    # validation (shared)
    # ------------------------------------------------------------------

    def validate_inputs(self):
        """Check inputs and return an exit code if anything is invalid."""
        cfg = self.inputs.structure_config.get_dict()

        if "protos" not in cfg or not cfg["protos"]:
            return self.exit_codes.ERROR_INVALID_STRUCTURE_CONFIG

        potentials_clean = [
            p for p in self.inputs.potentials_list.get_list()
            if isinstance(p, str) and p.strip()
        ]
        if not potentials_clean:
            return self.exit_codes.ERROR_EMPTY_POTENTIALS_LIST

        from aiida_batch.utils.structure import CONFIG, FIXED_1D_REP

        known = set(CONFIG) | set(FIXED_1D_REP)
        unknown = [p for p in cfg["protos"] if p not in known]
        if unknown:
            self.report(f"Unknown prototypes: {unknown}. Known: {sorted(known)}")
            return self.exit_codes.ERROR_INVALID_PROTOS

        return None

    # ------------------------------------------------------------------
    # submission loop (template)
    # ------------------------------------------------------------------

    def _build_child_inputs(self, potential: str, proto: str, atoms) -> dict:
        """Return the inputs dict for a single child workchain.

        Subclasses **must** override this.  It receives the current potential
        family label, prototype name and the ``ase.Atoms`` object.  The
        returned dict is passed directly to ``self.submit(ChildWorkChain, **inputs)``.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement _build_child_inputs"
        )

    def submit_children(self):
        cfg = self.inputs.structure_config.get_dict()
        potentials_list = [
            p for p in self.inputs.potentials_list.get_list()
            if isinstance(p, str) and p.strip()
        ]
        potentials_max = self.inputs.potentials_max.value
        structure_max = self.inputs.structure_max.value

        atoms_dict = self._generate_structures(
            protos=cfg["protos"],
            element=cfg.get("element", "U"),
            to_primitive=cfg.get("to_primitive", False),
            symprec=cfg.get("symprec", 1e-5),
        )
        all_protos = list(atoms_dict.keys())

        self.ctx.children_info = []

        for potential in potentials_list[:potentials_max]:
            for proto in all_protos[:structure_max]:
                atoms = atoms_dict[proto]
                label = f"{potential}_{proto}"

                if self.inputs.dry_run.value:
                    self.report(
                        f"[DRY-RUN] Would submit: potential={potential}, "
                        f"proto={proto}, natoms={len(atoms)}, label={label}"
                    )
                    continue

                inputs = self._build_child_inputs(potential, proto, atoms)
                child_cls = self._get_child_workchain_class()

                running = self.submit(child_cls, **inputs)
                running.base.extras.set_many({
                    "potential_family": potential,
                    "structure_name": proto,
                })
                self.ctx.children_info.append(
                    {"potential": potential, "proto": proto, "node": running}
                )
                self.to_context(children=append_(running))

    @staticmethod
    def _generate_structures(protos, element, to_primitive=False, symprec=1e-5):
        """Generate structures for the given prototypes."""
        from aiida_batch.utils.structure import generate_by_protos
        return generate_by_protos(
            protos=protos,
            element=element,
            to_primitive=to_primitive,
            symprec=symprec,
        )

    # ------------------------------------------------------------------
    # gather results (shared)
    # ------------------------------------------------------------------

    def gather_results(self):
        if self.inputs.dry_run.value:
            potentials = [
                p for p in self.inputs.potentials_list.get_list()
                if isinstance(p, str) and p.strip()
            ]
            cfg = self.inputs.structure_config.get_dict()
            n_protos = min(len(cfg["protos"]), self.inputs.structure_max.value)
            n_potentials = min(len(potentials), self.inputs.potentials_max.value)
            total_est = n_protos * n_potentials
            self.report(f"[DRY-RUN] Would submit {total_est} calculation(s) in total.")
            return ExitCode(0)

        info = self.ctx.children_info
        results = []
        n_ok = 0
        n_failed = 0

        for item in info:
            node = item["node"]
            ok = node.is_finished_ok
            exit_status = node.exit_status
            results.append({
                "potential": item["potential"],
                "proto": item["proto"],
                "pk": node.pk,
                "exit_status": exit_status,
                "ok": ok,
            })
            if ok:
                n_ok += 1
            else:
                n_failed += 1

        result_node = orm.Dict(dict={"children": results})
        result_node.store()
        self.out("results", result_node)

        self.report(
            f"Finished: {n_ok} OK, {n_failed} failed "
            f"(out of {len(info)} total)."
        )

        if n_failed == 0:
            return ExitCode(0)
        elif n_ok == 0:
            return self.exit_codes.ERROR_ALL_FAILED  # 302
        else:
            return self.exit_codes.WARNING_PARTIAL_FAILURE  # 301

    # ------------------------------------------------------------------
    # Config-file → AiiDA inputs  (classmethod, used by cli/run.py)
    # ------------------------------------------------------------------

    @classmethod
    def build_inputs_from_config(cls, cfg: dict) -> dict:
        """Build workchain inputs from a YAML/JSON config dict.

        Override in subclasses to add child-specific input handling.
        This base implementation handles the common batch inputs.
        """
        inp = cfg.get("inputs", {})
        return {
            "structure_config": orm.Dict(dict=inp.get("structure_config", {})),
            "potentials_list": orm.List(list=inp.get("potentials_list", [])),
            "potentials_max": orm.Int(inp.get("potentials_max", 99999)),
            "structure_max": orm.Int(inp.get("structure_max", 99999)),
            "dry_run": orm.Bool(inp.get("dry_run", False)),
        }

    @staticmethod
    def _build_vasp_namespace(vasp_cfg: dict) -> dict:
        """Helper: build the VASP input namespace from a config sub-dict.

        Handles *code*, *parameters* (incar), *kpoints*, *potential_family*, 
        *potential_mapping*, *kpoints_spacing*, *calc*.
        """
        from aiida.orm import Dict, load_code

        result = {}

        # code
        if "code" in vasp_cfg:
            code_label = vasp_cfg["code"]
            if isinstance(code_label, str):
                result["code"] = load_code(code_label)
            else:
                result["code"] = code_label

        # parameters (Dict containing incar)
        if "parameters" in vasp_cfg:
            result["parameters"] = Dict(dict=vasp_cfg["parameters"])

        # kpoints (KpointsData)
        if "kpoints" in vasp_cfg:
            from aiida.orm import KpointsData
            kp = KpointsData()
            if isinstance(vasp_cfg["kpoints"], dict):
                if "mesh" in vasp_cfg["kpoints"]:
                    kp.set_kpoints_mesh(**vasp_cfg["kpoints"]["mesh"])
                elif "path" in vasp_cfg["kpoints"]:
                    kp.set_kpoints_path(**vasp_cfg["kpoints"]["path"])
            result["kpoints"] = kp

        # kpoints_spacing
        if "kpoints_spacing" in vasp_cfg:
            result["kpoints_spacing"] = orm.Float(vasp_cfg["kpoints_spacing"])

        # potential settings
        if "potential_family" in vasp_cfg:
            result["potential_family"] = orm.Str(vasp_cfg["potential_family"])

        if "potential_mapping" in vasp_cfg:
            result["potential_mapping"] = Dict(dict=vasp_cfg["potential_mapping"])

        # calc (contains metadata.options)
        if "calc" in vasp_cfg:
            result["calc"] = vasp_cfg["calc"]

        return result
