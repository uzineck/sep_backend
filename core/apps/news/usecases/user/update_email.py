from dataclasses import dataclass

from core.apps.news.entities.user import User as ClientEntity
from core.apps.news.entities.token import Token as TokenEntity
from core.apps.news.services.user import BaseClientService
from core.apps.common.auth.validators.email import BaseEmailValidatorService


@dataclass
class UpdateClientEmailUseCase:
    client_service: BaseClientService

    email_validator_service: BaseEmailValidatorService

    def execute(self, old_email: str, new_email: str, password: str) -> tuple[ClientEntity, TokenEntity]:
        client = self.client_service.get_by_email(client_email=old_email)
        self.client_service.validate_password(client_password=client.password, plain_password=password)

        self.email_validator_service.validate(email=new_email, old_email=old_email)

        self.client_service.update_email(client_id=client.id, email=new_email)
        updated_client = self.client_service.get_by_id(client_id=client.id)

        tokens: TokenEntity = self.client_service.generate_tokens(client=updated_client)

        return updated_client, tokens
