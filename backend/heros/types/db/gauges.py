from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Callable, Optional, Self

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic import ValidationError, WrapValidator
from pydantic.functional_validators import ModelWrapValidatorHandler

from heros.logging import LOGGER


def invalid_to_none(v: Any, handler: Callable[[Any], Any]) -> Any:
    try:
        return handler(v)
    except ValidationError:
        LOGGER.error(f"Unable to convert {v}")
        return None


class GaugeData(BaseModel):
    """
    Gauge Data in the db.
    """

    @model_validator(mode="wrap")
    @classmethod
    def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        try:
            return handler(data)
        except ValidationError:
            LOGGER.error("Model %s failed to validate with data %s", cls, data)
            raise

    time: datetime
    data: Optional[float]
