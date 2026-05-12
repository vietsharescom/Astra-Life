import json
from pathlib import Path
from typing import Dict, Any

from core.exceptions import ContractViolationError


class ContractEnforcer:
    """
    Enforces module execution contracts defined in module_contracts.json
    """

    def __init__(self, contract_path: str):
        self.contract_path = Path(contract_path)
        self.raw_contract: Dict[str, Any] = self._load_contract_file()
        self.modules: Dict[str, Dict[str, Any]] = self._load_modules_section()

    # ---------- Public API ----------

    def validate_module_execution(
        self,
        module_name: str,
        stage: str,
        input_schema: str,
        output_schema: str,
    ) -> None:
        contract = self._get_module_contract(module_name)

        self._validate_stage(module_name, stage, contract)
        self._validate_input_schema(module_name, input_schema, contract)
        self._validate_output_schema(module_name, output_schema, contract)

    # ---------- Loaders ----------

    def _load_contract_file(self) -> Dict[str, Any]:
        if not self.contract_path.exists():
            raise FileNotFoundError(
                f"Module contract file not found: {self.contract_path}"
            )

        with self.contract_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("module_contracts.json must be a JSON object")

        return data

    def _load_modules_section(self) -> Dict[str, Dict[str, Any]]:
        if "modules" not in self.raw_contract:
            raise ValueError(
                "module_contracts.json missing required top-level key: 'modules'"
            )

        modules = self.raw_contract["modules"]

        if not isinstance(modules, dict):
            raise ValueError("'modules' must be a JSON object")

        return modules

    # ---------- Validators ----------

    def _get_module_contract(self, module_name: str) -> Dict[str, Any]:
        if module_name not in self.modules:
            raise ContractViolationError(
                f"Unknown module '{module_name}'. "
                f"Declared modules: {sorted(self.modules.keys())}"
            )

        return self.modules[module_name]

    def _validate_stage(
        self, module_name: str, stage: str, contract: Dict[str, Any]
    ) -> None:
        allowed = contract.get("allowed_stages")

        if not allowed:
            raise ContractViolationError(
                f"Module '{module_name}' does not declare 'allowed_stages'"
            )

        if stage not in allowed:
            raise ContractViolationError(
                f"Module '{module_name}' is not allowed to execute at stage '{stage}'. "
                f"Allowed stages: {allowed}"
            )

    def _validate_input_schema(
        self, module_name: str, input_schema: str, contract: Dict[str, Any]
    ) -> None:
        expected = contract.get("input_schema")

        if not expected:
            raise ContractViolationError(
                f"Module '{module_name}' does not declare 'input_schema'"
            )

        if expected != input_schema:
            raise ContractViolationError(
                f"Module '{module_name}' received invalid input schema '{input_schema}'. "
                f"Expected: '{expected}'"
            )

    def _validate_output_schema(
        self, module_name: str, output_schema: str, contract: Dict[str, Any]
    ) -> None:
        expected = contract.get("output_schema")

        if not expected:
            raise ContractViolationError(
                f"Module '{module_name}' does not declare 'output_schema'"
            )

        if expected != output_schema:
            raise ContractViolationError(
                f"Module '{module_name}' produced invalid output schema '{output_schema}'. "
                f"Expected: '{expected}'"
            )