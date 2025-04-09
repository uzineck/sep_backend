import punq

from core.apps.common.auth.password import BasePasswordService, BcryptPasswordService
from core.apps.common.auth.token import BaseTokenService, JWTTokenService
from core.apps.news.services.user import BaseClientService, ORMClientService
from core.apps.news.usecases.user.create import CreateClientUseCase
from core.apps.news.usecases.user.get_info import GetClientInfoUseCase
from core.apps.news.usecases.user.login import LoginClientUseCase
from core.apps.news.usecases.user.logout import LogoutClientUseCase
from core.apps.news.usecases.user.update_access_token import UpdateAccessTokenUseCase
from core.apps.news.usecases.user.update_credentials import UpdateClientCredentialsUseCase
from core.apps.news.usecases.user.update_email import UpdateClientEmailUseCase
from core.apps.news.usecases.user.update_password import UpdateClientPasswordUseCase
from core.apps.news.usecases.user.update_score import UpdateClientScoreUseCase


def register_client_services(container: punq.Container):
    container.register(BaseClientService, ORMClientService)
    container.register(BasePasswordService, BcryptPasswordService)
    container.register(BaseTokenService, JWTTokenService)

    container.register(CreateClientUseCase)
    container.register(LoginClientUseCase)
    container.register(LogoutClientUseCase)
    container.register(UpdateClientEmailUseCase)
    container.register(UpdateClientPasswordUseCase)
    container.register(UpdateClientCredentialsUseCase)
    container.register(GetClientInfoUseCase)
    container.register(UpdateAccessTokenUseCase)
    container.register(UpdateClientScoreUseCase)
