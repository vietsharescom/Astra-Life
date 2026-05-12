from typing import Any

from core.stage_result import StageResult


# =========================
# EXCEPTIONS
# =========================

class ExecutionEnforcerError(Exception):
    """
    Base execution enforcement error.
    """
    pass


class ContractViolationError(ExecutionEnforcerError):
    """
    Raised when ASTRA runtime contract is violated.
    """
    pass


# =========================
# EXECUTION ENFORCER
# =========================

class ExecutionEnforcer:
    """
    ASTRA LIFE v1.0 — L4.5 FINAL CONTRACT GATE

    ROLE:
    - Deep scan runtime outputs
    - Prevent StageResult leakage
    - Guarantee safe execution boundary

    PRINCIPLES:
    - Single-pass recursive validation
    - No duplicated validation layers
    - Root StageResult allowed ONLY inside executor boundary
    """

    # =========================
    # PUBLIC API
    # =========================

    def validate(self, data: Any) -> Any:
        """
        Validate runtime output boundary.
        """

        self._scan(data, path="root")

        return data

    # =========================
    # INTERNAL SCANNER
    # =========================

    def _scan(self, obj: Any, path: str) -> None:
        """
        Recursive ASTRA contract scanner.
        """

        # =====================================
        # RULE 1
        # Root StageResult is ALLOWED
        # but must recursively validate output
        # =====================================

        if isinstance(obj, StageResult):

            self._scan(
                obj.output,
                path=f"{path}.output"
            )

            return

        # =====================================
        # RULE 2
        # Deep scan dict
        # =====================================

        if isinstance(obj, dict):

            for k, v in obj.items():

                # nested StageResult NOT allowed
                if isinstance(v, StageResult):
                    raise ContractViolationError(
                        f"ASTRA VIOLATION: StageResult leakage at {path}.{k}"
                    )

                self._scan(v, f"{path}.{k}")

            return

        # =====================================
        # RULE 3
        # Deep scan list
        # =====================================

        if isinstance(obj, list):

            for i, v in enumerate(obj):

                # nested StageResult NOT allowed
                if isinstance(v, StageResult):
                    raise ContractViolationError(
                        f"ASTRA VIOLATION: StageResult leakage at {path}[{i}]"
                    )

                self._scan(v, f"{path}[{i}]")

            return

        # =====================================
        # RULE 4
        # Primitive / safe object
        # =====================================

        return