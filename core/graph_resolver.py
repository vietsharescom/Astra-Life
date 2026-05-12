from typing import Dict, Any, Optional
from core.pipeline_guard import PipelineGuard


# =========================
# ASTRA v1.2 — GRAPH DECISION AUTHORITY
# =========================

class GraphResolver:
    """
    ASTRA v1.2 — SINGLE SOURCE OF TRUTH FOR ROUTING

    ROLE:
    - Decide next_stage
    - Interpret graph_registry.json via PipelineGuard
    - Resolve conditional routing (future AI layer hook)

    DOES NOT:
    - execute logic
    - mutate state
    - validate contracts (Guard handles this)
    """

    def __init__(self, guard: PipelineGuard):
        self.guard = guard

    # =========================
    # MAIN RESOLUTION LOGIC
    # =========================

    def resolve_next_stage(
        self,
        current_stage: str,
        execution_result: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:

        """
        RULE:
        - default = linear graph
        - future = conditional routing via execution_result
        """

        context = context or {}
        execution_result = execution_result or {}

        # =========================
        # BASE GRAPH NEXT
        # =========================
        next_stage = self.guard.next(current_stage)

        if next_stage is None:
            return None

        # =========================
        # FUTURE HOOK (SEMANTIC ROUTING)
        # =========================
        # Example extension:
        # if execution_result.get("route") == "recovery":
        #     return "L8_RECOVERY"

        if execution_result.get("force_recovery"):
            return "L8_RECOVERY"

        if execution_result.get("skip"):
            # skip one step in graph
            return self.guard.next(next_stage)

        return next_stage