import json
import os
from typing import Dict, Any, List


# =========================
# EXCEPTIONS
# =========================

class PipelineInitializationError(Exception):
    pass


class PipelineTransitionError(Exception):
    pass


# =========================
# ASTRA v1.2 — GRAPH ENFORCEMENT AUTHORITY
# =========================

class PipelineGuard:
    """
    ASTRA v1.2 — GRAPH ENFORCEMENT AUTHORITY (UPDATED)

    ROLE:
    - Enforce legal graph transitions (DAG-based)
    - Validate runtime execution edges
    - Prevent invalid routing

    DOES NOT:
    - own state
    - execute logic
    - decide routing
    - mutate runtime
    """

    def __init__(
        self,
        stage_order_path: str,
        graph_registry_path: str | None = None
    ):

        self.stage_order_path = stage_order_path
        self.graph_registry_path = graph_registry_path

        # backward compatible (v1.0 fallback)
        self.stage_sequence = self._load_stage_order()

        # NEW: graph-based runtime (v1.2)
        self.graph_registry = self._load_graph_registry()

    # =========================
    # INITIALIZE
    # =========================

    def initialize(self) -> str:
        return self.stage_sequence[0]

    # =========================
    # LEGACY LINEAR NEXT (COMPAT ONLY)
    # =========================

    def next(self, current_stage: str):

        if current_stage not in self.stage_sequence:
            raise PipelineTransitionError(
                f"Unknown stage: {current_stage}"
            )

        idx = self.stage_sequence.index(current_stage)

        if idx + 1 >= len(self.stage_sequence):
            return None

        return self.stage_sequence[idx + 1]

    # =========================
    # GRAPH-BASED NEXT (v1.2 CORE)
    # =========================

    def allowed_next(self, current_stage: str) -> List[str]:

        if current_stage not in self.graph_registry:
            raise PipelineTransitionError(
                f"Unknown stage in graph: {current_stage}"
            )

        return self.graph_registry[current_stage]

    # =========================
    # VALIDATE TRANSITION (GRAPH-AWARE)
    # =========================

    def validate_transition(
        self,
        current_stage: str,
        to_stage: str,
        context: Dict[str, Any] | None = None
    ) -> bool:

        context = context or {}

        # =========================
        # VALID TARGET CHECK
        # =========================
        if to_stage not in self.stage_sequence:
            raise PipelineTransitionError(
                f"Invalid stage (not in system): {to_stage}"
            )

        # =========================
        # INITIAL ENTRY RULE
        # =========================
        if current_stage is None:

            expected = self.stage_sequence[0]

            if to_stage != expected:
                raise PipelineTransitionError(
                    f"Pipeline must start at {expected}"
                )

            return True

        # =========================
        # CURRENT VALIDATION
        # =========================
        if current_stage not in self.graph_registry:
            raise PipelineTransitionError(
                f"Unknown current stage: {current_stage}"
            )

        # =========================
        # GRAPH EDGE VALIDATION (CORE v1.2)
        # =========================
        allowed = self.allowed_next(current_stage)

        if to_stage not in allowed:
            raise PipelineTransitionError(
                f"Invalid transition: {current_stage} -> {to_stage}. "
                f"Allowed: {allowed}"
            )

        return True

    # =========================
    # LOAD LINEAR STAGE ORDER (BACKWARD COMPAT)
    # =========================

    def _load_stage_order(self):

        if not os.path.exists(self.stage_order_path):
            raise PipelineInitializationError(
                f"Stage order file not found: {self.stage_order_path}"
            )

        with open(self.stage_order_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):

            if "stages" not in data:
                raise PipelineInitializationError(
                    "Missing 'stages' key"
                )

            stages = data["stages"]

            if not isinstance(stages, list):
                raise PipelineInitializationError(
                    "'stages' must be a list"
                )

            return stages

        if isinstance(data, list):
            return data

        raise PipelineInitializationError(
            "Invalid stage_order.json format"
        )

    # =========================
    # LOAD GRAPH REGISTRY (v1.2 CORE)
    # =========================

    def _load_graph_registry(self):

        # default fallback path (ASTRA v1.2 standard)
        path = self.graph_registry_path or \
            "config/runtime_rules/graph_registry.json"

        if not os.path.exists(path):
            raise PipelineInitializationError(
                f"Graph registry not found: {path}"
            )

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise PipelineInitializationError(
                "graph_registry.json must be a dict (DAG format)"
            )

        return data