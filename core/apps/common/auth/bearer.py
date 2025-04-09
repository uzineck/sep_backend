from ninja.security import HttpBearer

from core.apps.common.auth.auth_check import AuthCheck


class JWTBearer(AuthCheck, HttpBearer):
    pass
