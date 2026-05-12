from typing import List, Dict, Any
import time
import copy


class GraphRuntimeAudit:
    """
    ASTRA v1.2 — GRAPH RUNTIME AUDIT LEDGER

    ROLE:
    - Record every committed graph transition
    - Provide deterministic replay
    - Enable post-mortem graph forensics

    DOES NOT:
    - Decide routing
    - Validate graph legality
    - Execute logic
    - Mutate runtime state
    """

    def __init__(self):
        self._events: List[Dict[str, Any]] = []

    # =========================
    # RECORD TRANSITION FACT
    # =========================

    def record_transition(
        self,
        from_stage: str,
        to_stage: str,
        execution_result: Dict[str, Any] | None = None
    ) -> None:
        self._events.append({
            "timestamp": time.time(),
            "from": from_stage,
            "to": to_stage,
            "result": copy.deepcopy(execution_result)
        })

    # =========================
    # SNAPSHOT (AUDIT VIEW)
    # =========================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "total_transitions": len(self._events),
            "events": copy.deepcopy(self._events)
        }

    # =========================
    # REPLAY (GRAPH PATH ONLY)
    # =========================

    def replay(self) -> List[str]:
        if not self._events:
            return []

        path = [self._events[0]["from"]]
        for e in self._events:
            path.append(e["to"])
        return path

    # =========================
    # CLEAR (TEST ONLY)
    # =========================

    def clear(self) -> None:
        self._events.clear()