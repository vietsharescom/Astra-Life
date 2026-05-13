from core.pipeline_guard import PipelineGuard
from core.pipeline_executor import PipelineExecutor
from core.orchestrator import Orchestrator


def main():

    # =========================
    # BOOTSTRAP CORE
    # =========================
    guard = PipelineGuard()
    executor = PipelineExecutor()

    # ❌ KHÔNG TẠO StateMachine THỦ CÔNG NỮA

    orch = Orchestrator(
        guard=guard,
        executor=executor
    )

    # =========================
    # RUN TEST
    # =========================
    result = orch.run({
        "input": "test"
    })

    print("RESULT:", result)


if __name__ == "__main__":
    main()