"""
prompt_renderer.py
────────────────────────────────────────────────────────
ROLE:
    Presentation-only adapter.
    Convert structured system objects into LLM-readable prompts.

AUTHORITY:
    NONE (non-authoritative)
    This module MUST NOT:
        - enforce policy
        - validate schema
        - make decisions
        - access memory
        - call tools

DESIGN PRINCIPLES:
    - Stateless
    - Deterministic
    - Side-effect free
    - Read-only input
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────
# Exceptions (Presentation-level only)
# ──────────────────────────────────────────────────────

class PromptRenderError(Exception):
    """Raised when prompt rendering fails (presentation only)."""
    pass


# ──────────────────────────────────────────────────────
# Prompt Template Registry
# ──────────────────────────────────────────────────────

@dataclass(frozen=True)
class PromptTemplate:
    """
    Immutable prompt template.
    """
    name: str
    template: str
    description: Optional[str] = None


class PromptTemplateRegistry:
    """
    Registry of approved prompt templates.
    No dynamic modification allowed at runtime.
    """

    def __init__(self, templates: Dict[str, PromptTemplate]) -> None:
        self._templates = templates.copy()

    def get(self, name: str) -> PromptTemplate:
        if name not in self._templates:
            raise PromptRenderError(f"Unknown prompt template: {name}")
        return self._templates[name]


# ──────────────────────────────────────────────────────
# Prompt Renderer
# ──────────────────────────────────────────────────────

class PromptRenderer:
    """
    Render structured input into final LLM prompt text.

    INPUT:
        - structured dicts (already validated upstream)

    OUTPUT:
        - string prompt

    GUARANTEES:
        - No mutation of input
        - No inference
        - No validation
    """

    def __init__(self, registry: PromptTemplateRegistry) -> None:
        self._registry = registry

    def render(
        self,
        template_name: str,
        *,
        semantic_payload: Dict[str, Any],
        agent_input: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render prompt using a registered template.

        Parameters
        ----------
        template_name:
            Name of the prompt template
        semantic_payload:
            Output from Semantic Engine (UnifiedItem)
        agent_input:
            AgentInput (already policy-approved)
        context:
            Optional orchestration context (trace_id, etc.)
            MUST NOT affect logic, only formatting.

        Returns
        -------
        str
            Rendered prompt text
        """

        try:
            template = self._registry.get(template_name)

            payload = {
                "semantic": semantic_payload,
                "agent_input": agent_input,
                "context": context or {},
            }

            rendered = template.template.format(
                semantic=json.dumps(payload["semantic"], indent=2, ensure_ascii=False),
                agent_input=json.dumps(payload["agent_input"], indent=2, ensure_ascii=False),
                context=json.dumps(payload["context"], indent=2, ensure_ascii=False),
            )

            return rendered.strip()

        except KeyError as e:
            raise PromptRenderError(f"Missing placeholder in template: {e}") from e
        except Exception as e:
            logger.exception("Prompt rendering failed")
            raise PromptRenderError(str(e)) from e


# ──────────────────────────────────────────────────────
# Default Template Set (CAN be externalized later)
# ──────────────────────────────────────────────────────

DEFAULT_TEMPLATES = PromptTemplateRegistry(
    templates={
        "agent_base": PromptTemplate(
            name="agent_base",
            description="Base agent execution prompt",
            template=(
                "You are an execution agent.\n\n"
                "## Semantic Input\n"
                "{semantic}\n\n"
                "## Agent Instruction\n"
                "{agent_input}\n\n"
                "## Execution Context\n"
                "{context}\n\n"
                "Rules:\n"
                "- Follow agent instructions strictly\n"
                "- Do NOT invent data\n"
                "- Do NOT exceed approved scope\n"
            ),
        ),
        "response_generator": PromptTemplate(
            name="response_generator",
            description="Final user-facing response renderer",
            template=(
                "Convert the following structured result into a clear response.\n\n"
                "## Execution Result\n"
                "{agent_input}\n\n"
                "Constraints:\n"
                "- No fabrication\n"
                "- No policy inference\n"
                "- No new facts\n"
            ),
        ),
    }
)


# ──────────────────────────────────────────────────────
# Factory (explicit, no magic)
# ──────────────────────────────────────────────────────

def create_default_prompt_renderer() -> PromptRenderer:
    """
    Factory for default PromptRenderer.
    """
    return PromptRenderer(registry=DEFAULT_TEMPLATES)