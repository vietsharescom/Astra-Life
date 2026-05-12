from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum


# =========================
# STATUS CONTRACT
# =========================

class StageStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# =========================
# STAGE RESULT CONTRACT
# =========================

@dataclass(frozen=True)
class StageResult:
    """
    ASTRA LIFE v1.0 — CORE DATA CONTRACT LAYER

    ROLE:
    - Standard envelope between pipeline stages
    - Guarantees structured + traceable data flow

    ENFORCEMENT RULES:
    - output MUST be dict
    - NO nested StageResult allowed (hard contract)
    - metadata optional only
    """

    status: StageStatus
    output: Dict[str, Any]

    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # =========================
    # CONTRACT VALIDATION
    # =========================

    def __post_init__(self):
        self._validate_output()

    def _validate_output(self):
        """
        ASTRA CONTRACT ENFORCER (LEVEL DATA LAYER)
        """

        # 1. MUST be dict
        if not isinstance(self.output, dict):
            raise ValueError("ASTRA CONTRACT ERROR: output must be dict")

        # 2. BLOCK nested StageResult (critical rule)
        for k, v in self.output.items():
            if isinstance(v, StageResult):
                raise ValueError(
                    f"ASTRA CONTRACT VIOLATION: nested StageResult at key '{k}'"
                )

    # =========================
    # SAFE ACCESSORS
    # =========================

    def is_success(self) -> bool:
        return self.status == StageStatus.SUCCESS

    def unwrap(self) -> Dict[str, Any]:
        """
        SAFE boundary extraction for executor layer
        """
        return self.output