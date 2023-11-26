from pydantic import BaseModel
from typing import Self, Any, get_type_hints


class ResponseModel(BaseModel):
    @classmethod
    def from_obj(cls, obj: Any) -> Self:
        types = get_type_hints(cls)
        types.pop("__slots__", None)

        attributes: dict = {}
        for field, _type in types.items():
            value = (
                obj[field] if isinstance(obj, dict) else getattr(obj, field)
            )
            if issubclass(_type, ResponseModel):
                attributes[field] = _type.from_obj(value)
            else:
                attributes[field] = (
                    _type(value) if not isinstance(value, _type) else value
                )

        return cls(**attributes)


class EmptyResponse(ResponseModel):
    pass


class ErrorMessage(BaseModel):
    message: str


ErrorMessageResponse = {"model": ErrorMessage}
