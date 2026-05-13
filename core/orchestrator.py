from typing import Any, Dict, Optional

from core.pipeline_guard import PipelineGuard
from core.pipeline_executor import PipelineExecutor
from core.state_machine import StateMachine
from core.graph_resolver import GraphResolver

from audit.execution_proof import ExecutionProof
from audit.ledger_auditor import LedgerAuditor


class Orchestrator:

    def __init__(self, guard: PipelineGuard, executor: PipelineExecutor):
        self.guard = guard
        self.executor = executor

        self.graph = guard.graph

        self.state_machine = StateMachine(graph=self.graph)
        self.resolver = GraphResolver(guard)

        self._initialized = False

    def initialize(self):
        if not self.graph:
            raise RuntimeError("EMPTY GRAPH")

        entry = self.state_machine.initialize()
        self._initialized = True
        return entry

    def run(self, payload: Any) -> Dict[str, Any]:

        if not self._initialized:
            self.initialize()

        history = []
        current = self.state_machine.get_current_stage()

        while current is not None:

            next_stage = self.resolver.resolve_next_stage(current)

            if next_stage is None:
                break

            # validate
            self.guard.validate_transition(current, next_stage)

            result = self.executor.execute_stage(
                payload=payload,
                current_stage=current,
                next_stage=next_stage
            )

            self.state_machine.observe_execution(
                stage=current,
                input_data=payload,
                output_data=result,
                ok=result.get("ok", True)
            )

            self.state_machine.commit(next_stage)

            history.append({
                "stage": current,
                "result": result
            })

            current = next_stage

        trace = self.state_machine.get_execution_trace()

        ledger_audit = LedgerAuditor().audit_execution_trace(trace)

        proof = ExecutionProof.generate(
            trace=trace,
            graph_audits=[],
            ledger_audit=ledger_audit
        )

        return {
            "ok": True,
            "history": history,
            "final_stage": self.state_machine.get_current_stage(),
            "execution_proof": proof
        }

    def snapshot(self):
        return {
            "graph_size": len(self.graph),
            "initialized": self._initialized
        }