# audit/graph_auditor.py
import json
import time
from pathlib import Path

class GraphAuditor:
    def __init__(self, pipeline_config_path="config/pipeline_flow.json"):
        self.pipeline = self._load_pipeline(pipeline_config_path)
        self.stage_order = self._build_stage_order(self.pipeline)

    def _load_pipeline(self, path):
        with open(Path(path), "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_stage_order(self, pipeline):
        stages = pipeline["stages"]
        stages_sorted = sorted(stages, key=lambda s: s["order"])
        return {s["id"]: idx for idx, s in enumerate(stages_sorted)}

    def audit_transition(self, trace_id, current_stage, next_stage):
        ts = time.time()

        if current_stage not in self.stage_order:
            return self._violation(
                trace_id, current_stage, next_stage,
                "UNKNOWN_CURRENT_STAGE", ts
            )

        if next_stage not in self.stage_order:
            return self._violation(
                trace_id, current_stage, next_stage,
                "UNKNOWN_NEXT_STAGE", ts
            )

        cur_idx = self.stage_order[current_stage]
        next_idx = self.stage_order[next_stage]

        if next_idx != cur_idx + 1:
            return self._violation(
                trace_id, current_stage, next_stage,
                "ILLEGAL_GRAPH_TRANSITION", ts
            )

        return {
            "type": "GRAPH_AUDIT",
            "timestamp": ts,
            "trace_id": trace_id,
            "current_stage": current_stage,
            "next_stage": next_stage,
            "status": "PASS"
        }

    def _violation(self, trace_id, cur, nxt, reason, ts):
        return {
            "type": "GRAPH_AUDIT",
            "timestamp": ts,
            "trace_id": trace_id,
            "current_stage": cur,
            "next_stage": nxt,
            "status": "VIOLATION",
            "reason": reason
        }