"""
ASTRA LIFE v1.0
Schema Enforcer — Enforcement Core (NON-LOGICAL)

Responsibilities:
- Load canonical JSON Schemas (READ-ONLY)
- Validate payloads against schema
- Fail-fast on violation

STRICT RULES:
- NO mutation
- NO inference
- NO auto-fix
- NO business logic
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from jsonschema import Draft202012Validator, ValidationError


class SchemaViolation(Exception):
    """Raised when payload violates schema."""
    pass


class UnknownSchema(Exception):
    """Raised when schema name is not registered."""
    pass


class SchemaEnforcer:
    """
    Pure schema validation layer.
    """

    # Canonical schema names (SYSTEM LOCK)
    CANON_SCHEMAS = {
        "UnifiedItem": "UnifiedItem.schema.json",
        "RoutingDecision": "RoutingDecision.schema.json",
        "AgentInput": "AgentInput.schema.json",
        "AgentResult": "AgentResult.schema.json",
        "ToolCall": "ToolCall.schema.json",
        "Response": "Response.schema.json",
    }

    def __init__(self, schema_root: str | Path):
        """
        schema_root: path to config/schemas/
        """
        self.schema_root = Path(schema_root).resolve()
        self._validators: Dict[str, Draft202012Validator] = {}

        self._load_all()

    # ------------------------------------------------------------------ #
    # Loading (BOOT-TIME ONLY)
    # ------------------------------------------------------------------ #

    def _load_all(self) -> None:
        """
        Load and compile all canonical schemas.
        This must happen once at boot time.
        """
        for name, filename in self.CANON_SCHEMAS.items():
            schema_path = self.schema_root / filename

            if not schema_path.exists():
                raise FileNotFoundError(
                    f"[SchemaEnforcer] Missing canonical schema: {schema_path}"
                )

            with schema_path.open("r", encoding="utf-8") as f:
                schema = json.load(f)

            validator = Draft202012Validator(schema)
            self._validators[name] = validator

    # ------------------------------------------------------------------ #
    # Public API (RUNTIME)
    # ------------------------------------------------------------------ #

    def validate(self, schema_name: str, payload: Dict[str, Any]) -> None:
        """
        Validate payload against canonical schema.

        Raises:
        - UnknownSchema
        - SchemaViolation
        """
        if schema_name not in self._validators:
            raise UnknownSchema(
                f"[SchemaEnforcer] Schema '{schema_name}' is not registered"
            )

        validator = self._validators[schema_name]

        errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)

        if errors:
            raise SchemaViolation(
                self._format_errors(schema_name, errors)
            )

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _format_errors(schema_name: str, errors: list[ValidationError]) -> str:
        lines = [
            f"[SchemaEnforcer] Schema violation: {schema_name}",
            f"Total errors: {len(errors)}",
        ]

        for err in errors:
            path = ".".join(str(p) for p in err.path) or "<root>"
            lines.append(f" - {path}: {err.message}")

        return "\n".join(lines)