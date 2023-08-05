
class AuthorizationFailed(Exception):
    pass


class AuthenticationFailed(AuthorizationFailed):
    pass


class InsufficientPermissions(AuthorizationFailed):
    pass


class ConnectionError(AuthorizationFailed):
    pass
