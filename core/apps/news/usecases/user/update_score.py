from dataclasses import dataclass
from decimal import Decimal
from core.apps.news.entities.user import User as ClientEntity
from core.apps.news.services.user import BaseClientService


@dataclass
class UpdateClientScoreUseCase:
    client_service: BaseClientService

    def execute(self, email: str, liked: bool) -> ClientEntity:
        client = self.client_service.get_by_email(client_email=email)
        if liked:
            self.client_service.update_score(
                client_id=client.id,
                score=client.score + Decimal('0.01'),
            )
        if not liked:
            self.client_service.update_score(
                client_id=client.id,
                score=client.score - Decimal('0.01'),
            )
        updated_client = self.client_service.get_by_id(client_id=client.id)

        return updated_client
