from dataclasses import dataclass

from core.apps.news.entities.token import Token as TokenEntity
from core.apps.news.services.user import BaseClientService
from core.apps.common.exceptions import InvalidTokenTypeException
from core.apps.common.models import TokenType


@dataclass
class UpdateAccessTokenUseCase:
    client_service: BaseClientService

    def execute(self, token: str) -> TokenEntity:
        token_type = self.client_service.get_token_type_from_token(token=token)
        if token_type != TokenType.REFRESH:
            raise InvalidTokenTypeException

        client_email = self.client_service.get_client_email_from_token(token=token)
        client = self.client_service.get_by_email(client_email=client_email)

        device_id = self.client_service.get_device_id_from_token(token=token)
        token: TokenEntity = self.client_service.update_access_token(client=client, device_id=device_id)
        return token
