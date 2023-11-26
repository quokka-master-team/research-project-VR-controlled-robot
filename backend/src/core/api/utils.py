from typing import Callable, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from functools import wraps
from fastapi import status


StatusCode = int


def make_response(
    response_model: Any, status_code: StatusCode = status.HTTP_200_OK
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> JSONResponse:
            result = await func(*args, **kwargs)
            content = (
                [
                    jsonable_encoder(response_model.from_obj(record))
                    for record in result
                ]
                if isinstance(result, list)
                else jsonable_encoder(response_model.from_obj(result))
            )
            return JSONResponse(content, status_code=status_code)

        return wrapper

    return decorator
