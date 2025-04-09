from dataclasses import dataclass

from core.apps.news.entities.user import User as ClientEntity
from core.apps.news.services.user import BaseClientService


@dataclass
class GetClientInfoUseCase:
    client_service: BaseClientService

    def execute(self, email: str) -> ClientEntity:
        client = self.client_service.get_by_email(client_email=email)

        return client
