from typing import Dict, Any, Optional
from core.pipeline_guard import PipelineGuard


# =========================
# ASTRA v1.2 — GRAPH DECISION AUTHORITY (GUARD-COMPATIBLE)
# =========================

class GraphResolver:
    """
    SINGLE SOURCE OF TRUTH FOR ROUTING

    RULES:
    - Routing strictly follows PipelineGuard graph
    - No state mutation
    - No execution
    - No payload interpretation
    """

    def __init__(self, guard: PipelineGuard):
        self.guard = guard

    # =========================
    # RESOLVE NEXT STAGE
    # =========================

    def resolve_next_stage(
        self,
        current_stage: str,
        execution_result: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:

        execution_result = execution_result or {}
        context = context or {}

        graph = self.guard.snapshot()

        # -------------------------
        # 1. VALIDATE CURRENT STAGE
        # -------------------------
        if current_stage not in graph:
            raise ValueError(
                f"[GraphResolver] Unknown current_stage: {current_stage}"
            )

        allowed_next = graph[current_stage]

        # -------------------------
        # 2. END OF GRAPH
        # -------------------------
        if not allowed_next:
            return None

        # default deterministic path
        next_stage = allowed_next[0]

        # -------------------------
        # 3. CONTROLLED OVERRIDES
        # -------------------------

        # force recovery only if graph allows
        if execution_result.get("force_recovery"):
            if "L8_RECOVERY" in allowed_next:
                return "L8_RECOVERY"

        # allow exactly ONE skip, still graph-bounded
        if execution_result.get("skip"):
            next_candidates = graph.get(next_stage, [])
            if next_candidates:
                return next_candidates[0]

        # -------------------------
        # 4. FINAL GRAPH INVARIANT
        # -------------------------
        if next_stage not in allowed_next:
            raise ValueError(
                f"[GraphResolver] Illegal transition: {current_stage} -> {next_stage}"
            )

        return next_stage

    # =========================
    # AUDIT SNAPSHOT (PHASE D READY)
    # =========================

    def snapshot(self) -> Dict[str, Any]:
        graph = self.guard.snapshot()
        return {
            "resolver": "GraphResolver",
            "version": "v1.2",
            "authority": "routing_only",
            "total_nodes": len(graph),
            "total_edges": sum(len(v) for v in graph.values())
        }