from typing import Any, Dict, List
from dataclasses import dataclass, field
import time


# =========================
# ASTRA v1.2 — EXECUTION LEDGER
# =========================

@dataclass
class LedgerEntry:
    stage: str
    payload: Any
    result: Any
    timestamp: float = field(default_factory=time.time)


class ExecutionLedger:
    """
    ASTRA GRAPH INTELLIGENCE LAYER CORE

    ROLE:
    - store full execution trace
    - enable replay
    - enable audit
    - deterministic reconstruction

    DOES NOT:
    - decide flow
    - execute logic
    - validate graph
    """

    def __init__(self):
        self.entries: List[LedgerEntry] = []

    # =========================
    # RECORD
    # =========================

    def record(self, stage: str, payload: Any, result: Any):

        self.entries.append(
            LedgerEntry(
                stage=stage,
                payload=payload,
                result=result
            )
        )

    # =========================
    # SNAPSHOT
    # =========================

    def snapshot(self) -> List[Dict[str, Any]]:

        return [
            {
                "stage": e.stage,
                "payload": e.payload,
                "result": e.result,
                "timestamp": e.timestamp
            }
            for e in self.entries
        ]

    # =========================
    # REPLAY CORE
    # =========================

    def replay(self):

        for entry in self.entries:
            yield entry