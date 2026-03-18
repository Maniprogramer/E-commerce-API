from fastapi import status


class AppError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "bad_request"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "bad_request"


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "unauthorized"
