from typing import Optional, List, Dict, Any
import copy

from core.pipeline_guard import PipelineGuard


# =========================
# EXCEPTIONS
# =========================

class StateMachineError(Exception):
    pass


class InvalidStateTransitionError(StateMachineError):
    pass


class StateMachineNotInitializedError(StateMachineError):
    pass


# =========================
# ASTRA v1.2 — STATE LEDGER + GRAPH INTELLIGENCE GATEWAY
# =========================

class StateMachine:
    """
    ASTRA v1.2 — EXECUTION LEDGER CORE

    ROLE:
    - lifecycle tracking
    - deterministic state ledger
    - execution trace storage (graph intelligence layer)
    - post-execution observation hook

    DOES NOT:
    - decide routing
    - execute business logic
    - interpret graph
    """

    def __init__(self, guard: PipelineGuard):

        self.guard = guard

        # =========================
        # CORE STATE
        # =========================
        self.current_stage: Optional[str] = None

        # =========================
        # HISTORY (STATE CHAIN)
        # =========================
        self.history: List[str] = []

        # =========================
        # GRAPH INTELLIGENCE LEDGER
        # =========================
        self.execution_context: List[Dict[str, Any]] = []

        # last execution snapshot
        self.last_payload: Any = None
        self.last_result: Any = None

        self.initialized: bool = False

    # =========================
    # INITIALIZE PIPELINE
    # =========================

    def initialize(self) -> str:

        stage = self.guard.initialize()

        self.current_stage = stage
        self.history = [stage]
        self.initialized = True

        return stage

    # =========================
    # STATE TRANSITION (COMMIT ONLY)
    # =========================

    def transition(
        self,
        next_stage: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:

        if not self.initialized:
            raise StateMachineNotInitializedError(
                "StateMachine not initialized."
            )

        # =========================
        # GRAPH VALIDATION (AUTHORITY = GUARD)
        # =========================
        self.guard.validate_transition(
            current_stage=self.current_stage,
            to_stage=next_stage,
            context=context or {}
        )

        # =========================
        # COMMIT STATE
        # =========================
        self.current_stage = next_stage
        self.history.append(next_stage)

        return self.current_stage

    # =========================
    # GRAPH INTELLIGENCE HOOK
    # =========================

    def observe_execution(
        self,
        stage: str,
        payload: Any,
        result: Any
    ) -> None:

        """
        ASTRA v1.2 KEY LAYER:
        - converts runtime execution into graph memory
        - enables replay + audit + deterministic reconstruction
        """

        self.last_payload = copy.deepcopy(payload)
        self.last_result = copy.deepcopy(result)

        self.execution_context.append({
            "stage": stage,
            "input": copy.deepcopy(payload),
            "output": copy.deepcopy(result)
        })

    # =========================
    # SNAPSHOT (REPLAY READY)
    # =========================

    def snapshot(self) -> Dict[str, Any]:

        return {
            "current_stage": self.current_stage,
            "history": copy.deepcopy(self.history),
            "initialized": self.initialized,

            # GRAPH INTELLIGENCE LAYER
            "execution_context": copy.deepcopy(self.execution_context),

            "last_payload": copy.deepcopy(self.last_payload),
            "last_result": copy.deepcopy(self.last_result)
        }

    # =========================
    # QUERY API
    # =========================

    def get_current_stage(self) -> Optional[str]:
        return self.current_stage

    def get_history(self) -> List[str]:
        return copy.deepcopy(self.history)

    def get_execution_trace(self) -> List[Dict[str, Any]]:
        return copy.deepcopy(self.execution_context)

    def is_initialized(self) -> bool:
        return self.initialized