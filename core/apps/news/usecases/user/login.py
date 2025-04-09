from dataclasses import dataclass

from core.apps.news.entities.token import Token as TokenEntity
from core.apps.news.entities.user import User as ClientEntity
from core.apps.news.services.user import BaseClientService


@dataclass
class LoginClientUseCase:
    client_service: BaseClientService

    def execute(self, email: str, password: str) -> tuple[ClientEntity, TokenEntity]:
        client = self.client_service.get_by_email(client_email=email)
        self.client_service.validate_password(client_password=client.password, plain_password=password)

        tokens: TokenEntity = self.client_service.generate_tokens(client=client)

        return client, tokens
