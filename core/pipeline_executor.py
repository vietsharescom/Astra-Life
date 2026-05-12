from typing import Any, Dict, Callable

from core.stage_result import StageResult
from core.pipeline_guard import PipelineGuard
from core.transition_policy import TransitionPolicy
from core.execution_enforcer import ExecutionEnforcer


# =========================
# EXCEPTIONS
# =========================

class PipelineExecutorError(Exception):
    pass


class StageNotRegisteredError(Exception):
    pass


class StageExecutionError(Exception):
    pass


# =========================
# ASTRA v1.2 — PURE EXECUTION ENGINE (GRAPH-AWARE SAFE)
# =========================

class PipelineExecutor:
    """
    ASTRA v1.2 — PURE EXECUTION ENGINE

    FINAL RULE:
    - NO state ownership
    - NO graph decision logic
    - NO routing authority
    - NO mutation of runtime state
    - ONLY executes + validates + sanitizes
    """

    def __init__(
        self,
        guard: PipelineGuard,
        stage_handlers: Dict[str, Callable]
    ):
        self.guard = guard
        self.stage_handlers = stage_handlers

        self.policy = TransitionPolicy()
        self.enforcer = ExecutionEnforcer()

    # =========================
    # EXECUTE STAGE (PURE COMPUTE ONLY)
    # =========================

    def execute_stage(
        self,
        payload: Any,
        current_stage: str,
        next_stage: str,
        context: Dict[str, Any] | None = None
    ) -> Any:

        context = context or {}

        # =========================================================
        # 🔴 FIX 1 — GRAPH CAPABILITY CHECK (ASTRA v1.2 COMPLIANCE)
        # =========================================================

        # 1. Verify current stage handler exists
        if current_stage not in self.stage_handlers:
            raise StageNotRegisteredError(
                f"[GRAPH CHECK FAIL] No handler registered for current stage: {current_stage}"
            )

        # 2. Verify next stage is executable (graph consistency check)
        if next_stage not in self.stage_handlers:
            raise StageNotRegisteredError(
                f"[GRAPH CHECK FAIL] No handler registered for next stage: {next_stage}"
            )

        handler = self.stage_handlers[current_stage]

        try:
            # =========================
            # NORMALIZE INPUT
            # =========================
            normalized_input = self.policy.normalize_input(payload)

            # safe enrichment only (NO decision logic)
            enriched_input = {
                "payload": normalized_input,
                "context": context,
                "current_stage": current_stage
            }

            # =========================
            # EXECUTE PURE HANDLER
            # =========================
            result = handler(enriched_input)

            # =========================
            # SANITIZE LEAKED STATE
            # =========================
            if isinstance(result, dict):
                result.pop("stage", None)
                result.pop("current_stage", None)
                result.pop("next_stage", None)
                result.pop("transition", None)

            # =========================
            # NORMALIZE OUTPUT
            # =========================
            normalized_output = self.policy.normalize_output(result)

            # =========================
            # CONTRACT ENFORCEMENT
            # =========================
            validated_output = self.enforcer.validate(normalized_output)

            # =========================
            # GRAPH VALIDATION (L4.5 ONLY - PRIMITIVE EDGE CHECK)
            # =========================
            self.guard.validate_transition(
                current_stage=current_stage,
                to_stage=next_stage,
                context=context
            )

        except Exception as e:
            raise StageExecutionError(
                f"Execution failed at stage {current_stage}: {e}"
            ) from e

        # =========================
        # RETURN PURE OUTPUT WRAPPER
        # =========================

        if isinstance(validated_output, StageResult):
            return {
                "output": validated_output.output,
                "ok": True
            }

        return {
            "output": validated_output,
            "ok": True
        }