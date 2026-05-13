from typing import Any, Dict, List, Optional
import time


class StateMachineError(Exception):
    pass


class InvalidCommitError(StateMachineError):
    pass


class StateMachine:
    """
    ASTRA v1.3 STATE MACHINE (FIXED)

    RULE:
    - Graph ALWAYS injected from PipelineGuard
    - NEVER allow empty graph
    """

    def __init__(self, graph: Dict[str, List[str]]):
        if not graph:
            raise InvalidCommitError("StateMachine requires non-empty graph")

        self._graph = graph
        self._initialized = False
        self._current_stage = None

        self._history: List[str] = []
        self._trace: List[Dict[str, Any]] = []

    def initialize(self) -> str:
        if self._initialized:
            raise InvalidCommitError("Already initialized")

        # ROOT = first key in graph (safe because guard already validated)
        entry = list(self._graph.keys())[0]

        self._current_stage = entry
        self._history.append(entry)
        self._initialized = True

        return entry

    def commit(self, next_stage: str) -> str:
        if not self._initialized:
            raise InvalidCommitError("Not initialized")

        self._current_stage = next_stage
        self._history.append(next_stage)

        return next_stage

    def observe_execution(self, stage: str, input_data: Any, output_data: Any, ok: bool):
        self._trace.append({
            "index": len(self._trace),
            "timestamp": time.time(),
            "stage": stage,
            "input": input_data,
            "output": output_data,
            "ok": ok
        })

    def get_current_stage(self):
        return self._current_stage

    def get_execution_trace(self):
        return list(self._trace)

    def get_graph_audit_events(self):
        return []

    def snapshot(self):
        return {
            "current_stage": self._current_stage,
            "history": self._history,
            "trace_size": len(self._trace)
        }