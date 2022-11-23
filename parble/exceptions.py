class ParbleException(Exception):
    pass


class ConfigurationError(ParbleException):
    pass


class APICallError(ParbleException):
    pass


class NotFoundError(APICallError):
    pass


class UnAuthorizedError(APICallError):
    pass


class CallTimeoutError(APICallError):
    pass


class InvalidCallError(APICallError):
    pass


handlers = {
    404: NotFoundError,
    401: UnAuthorizedError,
    400: InvalidCallError,
    500: APICallError,
}
