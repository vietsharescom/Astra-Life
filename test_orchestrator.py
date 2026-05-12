from typing import Any, Dict

from core.pipeline_guard import PipelineGuard
from core.pipeline_executor import PipelineExecutor
from core.state_machine import StateMachine


# =========================
# EXCEPTIONS
# =========================

class OrchestratorError(Exception):
    pass


class PipelineNotInitializedError(OrchestratorError):
    pass


class RoutingError(OrchestratorError):
    pass


# =========================
# ORCHESTRATOR (ASTRA v1.1)
# =========================

class Orchestrator:
    """
    ASTRA LIFE v1.1 — L5 Runtime Orchestrator

    ROLE:
    - Coordinate canonical pipeline flow
    - Propagate execution context
    - Wire Executor + Guard + StateMachine
    - Control explicit graph transition flow

    DOES NOT:
    - Implement business logic
    - Mutate payload schema
    - Validate contracts directly
    - Bypass PipelineGuard
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

        self.initialized = False

    # =========================
    # INITIALIZE
    # =========================

    def initialize(self) -> str:
        """
        Initialize runtime system.
        """

        entry_stage = self.state_machine.initialize()

        # sync executor stage
        self.executor.current_stage = entry_stage

        self.initialized = True

        return entry_stage

    # =========================
    # RUN SINGLE STAGE
    # =========================

    def run_stage(
        self,
        payload: Any,
        next_stage: str
    ) -> Any:
        """
        Execute current stage with explicit transition.

        ASTRA v1.1 RULE:
        - Transition MUST be explicit
        - Orchestrator propagates transition intent
        """

        if not self.initialized:
            raise PipelineNotInitializedError(
                "Orchestrator not initialized. Call initialize() first."
            )

        current_stage = self.state_machine.get_current_stage()

        if current_stage is None:
            raise RoutingError(
                "No active stage in StateMachine."
            )

        if not next_stage:
            raise RoutingError(
                "next_stage is required "
                "(ASTRA v1.1 explicit graph rule)"
            )

        # =========================
        # SYNC EXECUTOR STAGE
        # =========================

        self.executor.current_stage = current_stage

        # =========================
        # EXECUTE THROUGH L4.5
        # =========================

        result = self.executor.execute_stage(
            payload=payload,
            next_stage=next_stage
        )

        # =========================
        # RESYNC AFTER COMMIT
        # =========================

        self.executor.current_stage = (
            self.state_machine.get_current_stage()
        )

        return result

    # =========================
    # MANUAL MOVE
    # =========================

    def move_to(self, next_stage: str) -> str:
        """
        Manual transition control.

        WARNING:
        Normally NOT used in ASTRA v1.1 runtime flow,
        because executor already commits transitions.
        """

        if not self.initialized:
            raise PipelineNotInitializedError(
                "Orchestrator not initialized."
            )

        validated_stage = self.state_machine.transition(
            next_stage
        )

        self.executor.current_stage = validated_stage

        return validated_stage

    # =========================
    # EXECUTE + SNAPSHOT
    # =========================

    def run_and_move(
        self,
        payload: Any,
        next_stage: str
    ) -> Dict[str, Any]:
        """
        Execute stage and return runtime snapshot.

        IMPORTANT:
        - Executor already commits transition internally
        - DO NOT call move_to() again
        """

        result = self.run_stage(
            payload=payload,
            next_stage=next_stage
        )

        return {
            "result": result,
            "current_stage": self.state_machine.get_current_stage(),
            "history": self.state_machine.get_history()
        }

    # =========================
    # SNAPSHOT
    # =========================

    def snapshot(self) -> Dict[str, Any]:
        """
        Full runtime snapshot.
        """

        return {
            "initialized": self.initialized,
            "state_machine": self.state_machine.snapshot(),
            "executor_stage": self.executor.current_stage,
        }