from typing import Any, Dict, List
import time


# =========================
# ERRORS
# =========================

class StateMachineError(Exception):
    pass


class InvalidCommitError(StateMachineError):
    pass


# =========================
# ASTRA v1.2 — STATE MACHINE (LEDGER)
# =========================

class StateMachine:
    """
    ASTRA v1.2 — STATE LEDGER

    ROLE:
    - Track current stage
    - Record transition history
    - Record execution trace (replayable)

    DOES NOT:
    - Decide routing
    - Execute logic
    """

    def __init__(self):
        self._initialized = False
        self._current_stage: str | None = None
        self._history: List[str] = []
        self._trace: List[Dict[str, Any]] = []

    # =========================
    # INIT
    # =========================

    def initialize(self, entry_stage: str = "L0_INPUT") -> str:
        if self._initialized:
            raise InvalidCommitError("StateMachine already initialized")

        self._initialized = True
        self._current_stage = entry_stage
        self._history.append(entry_stage)
        return entry_stage

    # =========================
    # COMMIT TRANSITION
    # =========================

    def commit(self, next_stage: str) -> str:
        if not self._initialized:
            raise InvalidCommitError("StateMachine not initialized")

        self._current_stage = next_stage
        self._history.append(next_stage)
        return next_stage

    # =========================
    # OBSERVE EXECUTION (LEDGER RECORD)
    # =========================

    def observe_execution(
        self,
        stage: str,
        input_data: Any,
        output_data: Any,
        ok: bool
    ) -> None:

        record = {
            "index": len(self._trace),
            "timestamp": time.time(),
            "stage": stage,
            "input": input_data,
            "output": output_data,
            "ok": ok
        }

        self._trace.append(record)

    # =========================
    # READ-ONLY QUERIES
    # =========================

    def get_current_stage(self) -> str | None:
        return self._current_stage

    def get_history(self) -> List[str]:
        return list(self._history)

    def get_execution_trace(self) -> List[Dict[str, Any]]:
        return list(self._trace)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "initialized": self._initialized,
            "current_stage": self._current_stage,
            "history": list(self._history),
            "trace_size": len(self._trace),
        }