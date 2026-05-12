from core.pipeline_executor import PipelineExecutor
from core.pipeline_guard import PipelineGuard
from core.stage_result import StageResult, StageStatus


guard = PipelineGuard("config/runtime_rules/stage_order.json")

handlers = {
    # 🔥 L0: PASS THROUGH (CRITICAL ASTRA RULE)
    "L0_INPUT": lambda x: x,

    # 🔥 L1: semantic extraction
    "L1_SEMANTIC": lambda x: StageResult(
        status=StageStatus.SUCCESS,
        output={
            "text": x["raw"],
            "intent": "unknown",
            "entities": [],
            "confidence": 0.5
        }
    )
}

executor = PipelineExecutor(guard, handlers)

stage = executor.start()
print("START:", stage)

out = executor.execute_stage({"raw": "hello"})
print("L0:", out)

executor.move_to("L1_SEMANTIC")
out2 = executor.execute_stage(out)
print("L1:", out2)