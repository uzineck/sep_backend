from dataclasses import dataclass

from core.apps.news.services.user import BaseClientService


@dataclass
class LogoutClientUseCase:
    client_service: BaseClientService

    def execute(self, token: str) -> None:
        pass
        # client_email = self.client_service.get_client_email_from_token(token=token)
        # client = self.client_service.get_by_email(client_email=client_email)
