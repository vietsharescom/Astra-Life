from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class TransitionIntent:
    from_stage: str
    to_stage: str
    payload: Optional[Any] = None
    metadata: Optional[dict] = None