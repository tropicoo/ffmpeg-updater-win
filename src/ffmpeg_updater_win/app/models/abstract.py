"""Shared Pydantic model bases."""

from abc import ABC

from pydantic import BaseModel, ConfigDict


class BaseStrictConfigModel(BaseModel, ABC):
    """Frozen, strict config model that forbids extra fields."""

    model_config = ConfigDict(
        strict=True, frozen=True, extra='forbid', arbitrary_types_allowed=True
    )
    """Pydantic config: strict types, immutable instances, no extras."""
