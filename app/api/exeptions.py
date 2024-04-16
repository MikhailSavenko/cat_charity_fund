from http import HTTPStatus

from fastapi import HTTPException


class BadRequest(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class HttpNotFound(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)