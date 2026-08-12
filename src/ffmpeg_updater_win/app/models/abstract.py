from abc import ABC

from pydantic import BaseModel, ConfigDict


class BaseStrictConfigModel(BaseModel, ABC):
    model_config = ConfigDict(
        strict=True, frozen=True, extra='forbid', arbitrary_types_allowed=True
    )
