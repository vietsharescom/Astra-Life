from typing import Any, Dict

from core.pipeline_guard import PipelineGuard
from core.pipeline_executor import PipelineExecutor
from core.state_machine import StateMachine
from core.graph_resolver import GraphResolver
from core.graph_feedback import GraphFeedback


# =========================
# ERRORS
# =========================

class OrchestratorError(Exception):
    pass


class PipelineNotInitializedError(OrchestratorError):
    pass


class GraphResolutionError(OrchestratorError):
    pass


# =========================
# ASTRA v1.2 — GRAPH COORDINATOR (FINAL LOOP OWNER)
# =========================

class Orchestrator:
    """
    ASTRA v1.2 — CLOSED GRAPH LOOP COORDINATOR

    CORE RULES:
    - NO manual next_stage input
    - NO routing outside GraphResolver
    - NO execution decision in Orchestrator
    - Orchestrator = loop coordinator only
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
        self.feedback = GraphFeedback()

        self.initialized = False

    # =========================
    # INIT
    # =========================

    def initialize(self) -> str:
        entry = self.state_machine.initialize()
        self.initialized = True
        return entry

    # =========================
    # RUN (FULL CLOSED LOOP EXECUTION)
    # =========================

    def run_stage(self, payload: Any) -> Any:

        if not self.initialized:
            raise PipelineNotInitializedError()

        # =====================================================
        # 1. CURRENT STATE (SOURCE OF TRUTH)
        # =====================================================
        current_stage = self.state_machine.get_current_stage()

        # =====================================================
        # 2. GRAPH RESOLUTION (ONLY AUTHORITY FOR NEXT STEP)
        # =====================================================
        next_stage = self.resolver.resolve_next_stage(
            current_stage=current_stage,
            execution_result=None
        )

        if next_stage is None:
            return {"status": "END", "stage": current_stage}

        # =====================================================
        # 3. EXECUTION
        # =====================================================
        result = self.executor.execute_stage(
            payload=payload,
            current_stage=current_stage,
            next_stage=next_stage
        )

        # =====================================================
        # 4. STATE COMMIT (FACT RECORD ONLY)
        # =====================================================
        self.state_machine.transition(next_stage)

        # =====================================================
        # 5. FEEDBACK SIGNAL (EXECUTION → GRAPH LOOP)
        # =====================================================
        feedback_signal = self.feedback.evaluate(result, next_stage)

        # =====================================================
        # 6. REACTIVE GRAPH RESOLUTION (NO MANUAL CONTROL)
        # =====================================================
        refined_next_stage = self.resolver.resolve_next_stage(
            current_stage=next_stage,
            execution_result=feedback_signal
        )

        # =====================================================
        # 7. OPTIONAL SECOND HOP (ONLY IF GRAPH ALLOWS)
        # =====================================================
        if refined_next_stage and refined_next_stage != next_stage:

            second_result = self.executor.execute_stage(
                payload=payload,
                current_stage=next_stage,
                next_stage=refined_next_stage
            )

            self.state_machine.transition(refined_next_stage)

            return second_result

        # =====================================================
        # RETURN FINAL RESULT
        # =====================================================
        return result

    # =========================
    # SNAPSHOT
    # =========================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "initialized": self.initialized,
            "state_machine": self.state_machine.snapshot(),
            "resolver": "GraphResolver(active)",
            "feedback": "GraphFeedback(active)",
            "loop": "closed_v1.2"
        }