import logging

from rest_framework import exceptions, status, views

logger = logging.getLogger('main')


def custom_exception_handler(exc, context):
    response = views.exception_handler(exc, context)

    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    if response is not None:
        logger.warning("%s: %s", type(exc).__name__, exc)
    else:
        logger.exception("%s: %s", type(exc).__name__, exc)

    return response


class ValidateError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = 1

        detail = {"code": code, "detail": detail}
        self.detail = exceptions._get_error_details(detail, code)
