from core.apps.common.auth.bearer import JWTBearer
from core.apps.common.models import UserRole


jwt_auth_admin = JWTBearer([UserRole.ADMIN])
jwt_auth_manager = JWTBearer([UserRole.MANAGER])
jwt_auth_creator = JWTBearer([UserRole.CREATOR])

jwt_auth = JWTBearer([
    UserRole.ADMIN,
    UserRole.MANAGER,
    UserRole.CREATOR,
])
