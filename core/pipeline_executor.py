from typing import Any, Dict, Callable, Optional


# =========================
# ERRORS
# =========================

class StageNotRegisteredError(Exception):
    pass


# =========================
# ASTRA v1.2 — PIPELINE EXECUTOR
# =========================

class PipelineExecutor:
    """
    ASTRA v1.2 — EXECUTION ENGINE

    ROLE:
    - Execute stage logic ONLY
    - NO routing
    - NO graph decisions
    - NO state management
    """

    def __init__(
        self,
        guard=None,
        stage_handlers: Optional[Dict[str, Callable]] = None
    ):
        self.guard = guard

        # injected handlers OR fallback
        self.stage_handlers = stage_handlers or self._default_handlers()

    # =========================
    # DEFAULT HANDLERS (SAFE FALLBACK)
    # =========================

    def _default_handlers(self) -> Dict[str, Callable]:
        """
        Prevent system crash when no handlers are provided
        """

        return {
            "L0_INPUT": self._default_handler,
            "L1": self._default_handler,
            "L2": self._default_handler,
            "DEFAULT": self._default_handler
        }

    def _default_handler(self, payload: Any) -> Dict[str, Any]:
        return {
            "ok": True,
            "data": payload,
            "message": "default execution"
        }

    # =========================
    # EXECUTE STAGE
    # =========================

    def execute_stage(
        self,
        payload: Any,
        current_stage: str,
        next_stage: Optional[str] = None
    ) -> Dict[str, Any]:

        handler = self.stage_handlers.get(current_stage)

        # fallback safety (NO CRASH MODE)
        if handler is None:
            handler = self.stage_handlers.get("DEFAULT")

        if handler is None:
            raise StageNotRegisteredError(
                f"[GRAPH CHECK FAIL] No handler registered for current stage: {current_stage}"
            )

        try:
            result = handler(payload)

            # normalize output
            if not isinstance(result, dict):
                result = {"ok": True, "data": result}

            return result

        except Exception as e:
            return {
                "ok": False,
                "error": str(e),
                "stage": current_stage
            }