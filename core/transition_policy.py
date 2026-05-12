from typing import Any, Dict, Union
from core.stage_result import StageResult


class TransitionPolicy:
    """
    ASTRA LIFE v1.0 — CONTRACT ENFORCEMENT LAYER

    ROLE:
    - Normalize inputs before execution
    - Normalize outputs after execution
    - Prevent structural drift across pipeline

    DOES NOT:
    - Execute logic
    - Decide flow
    - Validate business rules
    """

    # =========================
    # INPUT NORMALIZATION
    # =========================

    def normalize_input(self, payload: Any) -> Dict[str, Any]:
        """
        Ensure handler always receives safe dict input
        """

        if isinstance(payload, StageResult):
            # unwrap safely
            return payload.output

        if isinstance(payload, dict):
            return payload

        # fallback safe wrapper
        return {"value": payload}

    # =========================
    # OUTPUT NORMALIZATION
    # =========================

    def normalize_output(self, result: Any) -> Union[Dict[str, Any], StageResult]:
        """
        Ensure output follows ASTRA contract boundary
        """

        # Case 1: already StageResult → allow pass-through
        if isinstance(result, StageResult):
            return result

        # Case 2: dict → valid output
        if isinstance(result, dict):
            return result

        # Case 3: primitive → wrap safely
        return {"value": result}