from dataclasses import dataclass

from core.apps.news.entities.user import User as ClientEntity
from core.apps.news.services.user import BaseClientService
from core.apps.common.auth.password import BasePasswordService
from core.apps.common.auth.validators.email import BaseEmailValidatorService
from core.apps.common.auth.validators.password import BasePasswordValidatorService


@dataclass
class CreateClientUseCase:
    client_service: BaseClientService
    password_service: BasePasswordService

    password_validator_service: BasePasswordValidatorService
    email_validator_service: BaseEmailValidatorService

    def execute(
        self,
        first_name: str,
        last_name: str,
        middle_name: str,
        role: str,
        email: str,
        password: str,
        verify_password: str,
    ) -> ClientEntity:

        self.email_validator_service.validate(email=email)
        self.password_validator_service.validate(password=password, verify_password=verify_password)

        hashed_password = self.password_service.hash_password(plain_password=password)
        client = self.client_service.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role=role,
            email=email,
            hashed_password=hashed_password,
        )

        return client
