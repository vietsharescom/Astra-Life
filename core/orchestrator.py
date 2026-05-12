from typing import Any, Dict

from core.pipeline_guard import PipelineGuard
from core.pipeline_executor import PipelineExecutor
from core.state_machine import StateMachine
from core.graph_resolver import GraphResolver


# =========================
# ERRORS
# =========================

class OrchestratorError(Exception):
    pass


class PipelineNotInitializedError(OrchestratorError):
    pass


# =========================
# ASTRA v1.2 — GRAPH ORCHESTRATOR
# =========================

class Orchestrator:
    """
    ASTRA v1.2 — CLOSED GRAPH LOOP COORDINATOR

    RULES:
    - Orchestrator does NOT decide routing
    - Orchestrator does NOT execute logic
    - Orchestrator does NOT own state
    - Orchestrator only coordinates
    """

    def __init__(
        self,
        guard: PipelineGuard,
        executor: PipelineExecutor,
        state_machine: StateMachine
    ):
        self.guard = guard
        self.executor = executor
        self.state_machine = state_machine

        self.resolver = GraphResolver(guard)
        self._initialized = False

    # =========================
    # INIT
    # =========================

    def initialize(self) -> str:
        entry = self.state_machine.initialize()
        self._initialized = True
        return entry

    # =========================
    # RUN ONE STEP
    # =========================

    def run_stage(self, payload: Any) -> Dict[str, Any]:

        if not self._initialized:
            raise PipelineNotInitializedError("Orchestrator not initialized")

        # 1. CURRENT STAGE (LEDGER TRUTH)
        current_stage = self.state_machine.get_current_stage()

        # 2. GRAPH RESOLUTION
        next_stage = self.resolver.resolve_next_stage(
            current_stage=current_stage,
            execution_result=None
        )

        if next_stage is None:
            return {"status": "END", "stage": current_stage}

        # 3. EXECUTE CURRENT STAGE
        result = self.executor.execute_stage(
            payload=payload,
            current_stage=current_stage,
            next_stage=next_stage
        )

        # 4. RECORD EXECUTION (LEDGER)
        self.state_machine.observe_execution(
            current_stage,
            payload,
            result,
            result.get("ok", False)
        )

        # 5. COMMIT TRANSITION
        self.state_machine.commit(next_stage)

        return result

    # =========================
    # SNAPSHOT
    # =========================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "initialized": self._initialized,
            "state_machine": self.state_machine.snapshot(),
            "resolver": "GraphResolver(active)",
            "loop": "closed_v1.2"
        }