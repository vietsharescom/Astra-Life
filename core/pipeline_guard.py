from typing import Dict, List, Optional, Any
import json
import os


# =========================
# ERRORS
# =========================

class PipelineGuardError(Exception):
    pass


class IllegalTransitionError(PipelineGuardError):
    pass


class UnknownStageError(PipelineGuardError):
    pass


class TerminalStageError(PipelineGuardError):
    pass


# =========================
# ASTRA v1.3 — GRAPH AUTHORITY LAYER (STABLE)
# =========================

class PipelineGuard:
    """
    SINGLE SOURCE OF TRUTH FOR PIPELINE GRAPH
    """

    def __init__(self, graph_registry_path: Optional[str] = None):
        self.graph_registry_path = (
            graph_registry_path or self._default_registry_path()
        )

        # 🔥 LOAD + SNAPSHOT (CRITICAL FIX)
        self.graph: Dict[str, List[str]] = dict(self._load_graph())

        # 🔥 NORMALIZE GRAPH (ensure list copy)
        self.graph = {
            k: list(v) for k, v in self.graph.items()
        }

    # =========================
    # LOAD GRAPH
    # =========================

    def _default_registry_path(self) -> str:
        return os.path.join(
            os.getcwd(),
            "config",
            "runtime_rules",
            "graph_registry.json"
        )

    def _load_graph(self) -> Dict[str, List[str]]:
        if not os.path.exists(self.graph_registry_path):
            raise PipelineGuardError(
                f"Graph registry not found: {self.graph_registry_path}"
            )

        with open(self.graph_registry_path, "r", encoding="utf-8") as f:
            graph = json.load(f)

        if not isinstance(graph, dict):
            raise PipelineGuardError("Graph must be a dict")

        return graph

    # =========================
    # ROOT ENTRY (ROBUST)
    # =========================

    def initialize(self) -> str:
        if not self.graph:
            raise PipelineGuardError("Empty graph registry")

        # priority entry detection
        if "L0_INPUT" in self.graph:
            return "L0_INPUT"

        # fallback: first node with outgoing edges
        for k, v in self.graph.items():
            if isinstance(v, list):
                return k

        raise PipelineGuardError("No valid entry stage found")

    # =========================
    # VALIDATION
    # =========================

    def validate_transition(
        self,
        current_stage: str,
        to_stage: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:

        if current_stage not in self.graph:
            raise UnknownStageError(current_stage)

        allowed = self.graph.get(current_stage, [])

        if to_stage not in allowed:
            raise IllegalTransitionError(
                f"{current_stage} → {to_stage}"
            )

    # =========================
    # INTROSPECTION
    # =========================

    def allowed_edges(self, stage: str) -> List[str]:
        if stage not in self.graph:
            raise UnknownStageError(stage)
        return list(self.graph[stage])

    def is_terminal(self, stage: str) -> bool:
        if stage not in self.graph:
            raise UnknownStageError(stage)
        return len(self.graph[stage]) == 0

    def snapshot(self) -> Dict[str, List[str]]:
        return {k: list(v) for k, v in self.graph.items()}

    # =========================
    # COMPATIBILITY LAYER (CRITICAL FOR ORCHESTRATOR)
    # =========================

    @property
    def pipeline_spec(self) -> Dict[str, Any]:
        """
        FIXED FORMAT:
        - must be list[dict] with order + id
        - must be stable sorted by insertion order
        """

        stages = [
            {"id": k, "order": i}
            for i, k in enumerate(list(self.graph.keys()))
        ]

        return {
            "stages": stages,
            "graph": self.graph
        }