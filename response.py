import http
import typing


class ErrorResponse(Exception):
    def __init__(
        self,
        status_code: int = 400,
        detail: typing.Optional[str] = None,
        errorCode: typing.Optional[dict] = None,
        errorMessage: typing.Optional[dict] = None,
        cause: typing.Optional[str] = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        if errorCode is None:
            errorCode = status_code
        self.status_code = status_code
        self.detail = detail
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.cause = cause
