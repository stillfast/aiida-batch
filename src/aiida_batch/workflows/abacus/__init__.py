"""Batch-submit ABACUS calculations for multiple pseudos and structures.

Sub-modules
-----------
* :mod:`~aiida_batch.workflows.abacus.base` — child = ``abacus.base``
* :mod:`~aiida_batch.workflows.abacus.band` — child = ``abacus.band``

Entry points
------------
* ``abacus.base.batch``
* ``abacus.band.batch``

Exit codes
----------
    0 : All children finished successfully.
  301 : Some children failed (partial success).
  302 : All children failed.
  401 : Invalid *structure_config* (missing ``protos`` key).
  402 : *pseudos_list* is empty or only contains empty strings.
  403 : *structure_config.protos* contains unknown prototypes.
"""

from aiida.engine import WorkChain, ExitCode, append_
from aiida import orm
from aiida.plugins import WorkflowFactory
from aiida_batch.utils.structure import generate_by_protos
from aiida.orm import StructureData


# ===========================================================================
#  Base class — shared batch logic
# ===========================================================================


class AbacusBatchSubmitWorkChain(WorkChain):
    """Base batch-submit workchain for ABACUS.

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
            "pseudos_list",
            valid_type=orm.List,
            help="List of pseudo family labels (strings).",
        )
        spec.input(
            "pseudos_max",
            valid_type=orm.Int,
            required=False,
            default=lambda: orm.Int(99999),
            help="Max number of pseudo families to use.",
        )
        spec.input(
            "structure_max",
            valid_type=orm.Int,
            required=False,
            default=lambda: orm.Int(99999),
            help="Max number of structures to use per pseudo family.",
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
            "ERROR_EMPTY_PSEUDOS_LIST",
            message="pseudos_list is empty or contains only blank entries",
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

        pseudos_clean = [
            p for p in self.inputs.pseudos_list.get_list() if isinstance(p, str) and p.strip()
        ]
        if not pseudos_clean:
            return self.exit_codes.ERROR_EMPTY_PSEUDOS_LIST

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

    def _build_child_inputs(self, pseudo: str, proto: str, atoms) -> dict:
        """Return the inputs dict for a single child workchain.

        Subclasses **must** override this.  It receives the current pseudo
        family label, prototype name and the ``ase.Atoms`` object.  The
        returned dict is passed directly to ``self.submit(ChildWorkChain, **inputs)``.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement _build_child_inputs"
        )

    def submit_children(self):
        cfg = self.inputs.structure_config.get_dict()
        pseudos_list = [
            p for p in self.inputs.pseudos_list.get_list() if isinstance(p, str) and p.strip()
        ]
        pseudos_max = self.inputs.pseudos_max.value
        structure_max = self.inputs.structure_max.value

        atoms_dict = generate_by_protos(
            protos=cfg["protos"],
            element=cfg.get("element", "U"),
            to_primitive=cfg.get("to_primitive", False),
            symprec=cfg.get("symprec", 1e-5),
        )
        all_protos = list(atoms_dict.keys())

        self.ctx.children_info = []

        for pseudo in pseudos_list[:pseudos_max]:
            for proto in all_protos[:structure_max]:
                atoms = atoms_dict[proto]
                label = f"{pseudo}_{proto}"

                if self.inputs.dry_run.value:
                    self.report(
                        f"[DRY-RUN] Would submit: pseudo={pseudo}, "
                        f"proto={proto}, natoms={len(atoms)}, label={label}"
                    )
                    continue

                inputs = self._build_child_inputs(pseudo, proto, atoms)
                child_cls = self._get_child_workchain_class()

                running = self.submit(child_cls, **inputs)
                running.base.extras.set_many({
                    "pseudo_family": pseudo,
                    "structure_name": proto,
                })
                self.ctx.children_info.append(
                    {"pseudo": pseudo, "proto": proto, "node": running}
                )
                self.to_context(children=append_(running))

    # ------------------------------------------------------------------
    # gather results (shared)
    # ------------------------------------------------------------------

    def gather_results(self):
        if self.inputs.dry_run.value:
            pseudos = [
                p
                for p in self.inputs.pseudos_list.get_list()
                if isinstance(p, str) and p.strip()
            ]
            cfg = self.inputs.structure_config.get_dict()
            n_protos = min(len(cfg["protos"]), self.inputs.structure_max.value)
            n_pseudos = min(len(pseudos), self.inputs.pseudos_max.value)
            total_est = n_protos * n_pseudos
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
                "pseudo": item["pseudo"],
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
        from aiida import orm as _orm

        inp = cfg.get("inputs", {})
        return {
            "structure_config": _orm.Dict(dict=inp.get("structure_config", {})),
            "pseudos_list": _orm.List(list=inp.get("pseudos_list", [])),
            "pseudos_max": _orm.Int(inp.get("pseudos_max", 99999)),
            "structure_max": _orm.Int(inp.get("structure_max", 99999)),
            "dry_run": _orm.Bool(inp.get("dry_run", False)),
        }

    @staticmethod
    def _build_abacus_namespace(abacus_cfg: dict) -> dict:
        """Helper: build the ``abacus`` input namespace from a config sub-dict.

        Handles *code*, *parameters*, *pseudo_family*, *metadata*.
        """
        ns: dict = {}
        code_label = abacus_cfg.get("code")
        if code_label:
            from aiida.orm import load_code
            ns["code"] = load_code(code_label)
        if "parameters" in abacus_cfg:
            ns["parameters"] = orm.Dict(dict=abacus_cfg["parameters"])
        if "pseudo_family" in abacus_cfg:
            ns["pseudo_family"] = orm.Str(abacus_cfg["pseudo_family"])
        meta = abacus_cfg.get("metadata", {})
        if meta:
            ns["metadata"] = meta
        return ns
