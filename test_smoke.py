from core.pipeline_guard import PipelineGuard
from core.state_machine import StateMachine
from core.pipeline_executor import PipelineExecutor
from core.orchestrator import Orchestrator


# =========================
# INIT CORE SYSTEM
# =========================

guard = PipelineGuard("config/runtime_rules/stage_order.json")
sm = StateMachine(guard)

executor = PipelineExecutor(
    guard=guard,
    stage_handlers={
        "L0_INPUT": lambda x: {"ok": True},
        "L1_SEMANTIC": lambda x: {"ok": True},
    }
)

orch = Orchestrator(guard, executor, sm)


# =========================
# INIT PIPELINE
# =========================

print("INIT:", orch.initialize())


# ❌ KHÔNG MANUAL TRANSITION (ASTRA v1.2 RULE)
# sm.transition("L1_SEMANTIC")  ← REMOVED


# =========================
# RUN GRAPH-DRIVEN EXECUTION
# =========================

result = orch.run_stage({"x": 1})

print("RESULT:", result)


# =========================
# SNAPSHOT
# =========================

print("SNAPSHOT:", orch.snapshot())