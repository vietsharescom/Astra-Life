from typing import Any, Dict


class SemanticRoutingError(Exception):
    pass


class SemanticRouter:
    """
    ASTRA v1.1 — SEMANTIC INTELLIGENCE LAYER

    PURPOSE:
    - Convert raw input → semantic intent
    - Decide correct graph path BEFORE execution
    - Add intelligence above deterministic engine

    THIS IS NOT EXECUTION.
    THIS IS NOT STATE.
    THIS IS MEANING LAYER.
    """

    def __init__(self):
        # simple intent map (can upgrade to ML later)
        self.intent_map = {
            "simple": "L0_INPUT",
            "semantic": "L1_SEMANTIC",
            "complex": "L2_LOGIC"
        }

    # =========================
    # INTENT DETECTION
    # =========================

    def detect_intent(self, payload: Any) -> str:

        if not isinstance(payload, dict):
            return "simple"

        if "query" in payload or "text" in payload:
            return "semantic"

        if len(payload.keys()) > 2:
            return "complex"

        return "simple"

    # =========================
    # ROUTE DECISION
    # =========================

    def route(self, payload: Any) -> str:

        intent = self.detect_intent(payload)

        if intent not in self.intent_map:
            raise SemanticRoutingError(f"Unknown intent: {intent}")

        return self.intent_map[intent]

    # =========================
    # ENRICH CONTEXT
    # =========================

    def enrich(self, payload: Any) -> Dict[str, Any]:

        if isinstance(payload, dict):
            enriched = dict(payload)
        else:
            enriched = {"value": payload}

        enriched["intent"] = self.detect_intent(payload)
        enriched["route"] = self.route(payload)

        return enriched