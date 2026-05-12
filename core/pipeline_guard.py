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
# ASTRA v1.2 — GRAPH LEGALITY AUTHORITY
# =========================

class PipelineGuard:
    """
    ASTRA v1.2 — SINGLE SOURCE OF GRAPH LEGALITY

    ROLE:
    - Load canonical graph registry
    - Validate symbolic stage transitions
    - Enforce graph legality (DAG / loop / recovery)

    DOES NOT:
    - Decide routing
    - Execute logic
    - Mutate runtime state
    """

    def __init__(self, graph_registry_path: Optional[str] = None):
        self.graph_registry_path = graph_registry_path or self._default_registry_path()
        self.graph: Dict[str, List[str]] = self._load_graph()

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
            raise PipelineGuardError("Graph registry must be a dict")

        return graph

    # =========================
    # ENTRY POINT
    # =========================

    def initialize(self) -> str:
        """
        Entry stage = first key in graph registry
        """
        if not self.graph:
            raise PipelineGuardError("Empty graph registry")

        return list(self.graph.keys())[0]

    # =========================
    # GRAPH VALIDATION
    # =========================

    def validate_transition(
        self,
        current_stage: str,
        to_stage: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Validate whether transition is legal in the graph.
        """

        if current_stage not in self.graph:
            raise UnknownStageError(
                f"Unknown current stage: {current_stage}"
            )

        allowed_targets = self.graph[current_stage]

        if not allowed_targets:
            raise TerminalStageError(
                f"Stage {current_stage} is terminal; no outgoing transitions allowed"
            )

        if to_stage not in allowed_targets:
            raise IllegalTransitionError(
                f"Illegal transition: {current_stage} → {to_stage}"
            )

    # =========================
    # GRAPH INTROSPECTION (READ-ONLY)
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
        """
        Graph snapshot for audit / replay / tests
        """
        return {k: list(v) for k, v in self.graph.items()}