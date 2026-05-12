from typing import Any, Dict


class GraphFeedback:
    """
    ASTRA v1.2 — GRAPH FEEDBACK LAYER

    ROLE:
    - convert execution result → routing signal
    - provide feedback for GraphResolver
    - enable adaptive graph behavior

    DOES NOT:
    - execute logic
    - mutate state
    - replace Guard/Executor
    """

    def __init__(self):
        pass

    def evaluate(self, result: Any, current_stage: str) -> Dict[str, Any]:

        # default neutral signal
        signal = {
            "continue": True,
            "confidence": 1.0,
            "hint": None
        }

        # rule: failure pattern
        if isinstance(result, dict):

            if result.get("error") or result.get("ok") is False:
                signal["continue"] = False
                signal["hint"] = "RECOVERY"
                signal["confidence"] = 0.2

        return signal