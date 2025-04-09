import pytest
from test.factories.client.client import ClientModelFactory

from core.apps.news.entities.user import User as ClientEntity
from core.apps.common.auth.token import BaseTokenService
from core.apps.common.models import (
    UserRole,
    TokenType,
)


@pytest.fixture(scope='function')
def service_params(generate_device_id):
    client = ClientModelFactory.create(role=UserRole.CREATOR)
    client_entity = ClientEntity(
        id=client.id,
        first_name=client.first_name,
        last_name=client.last_name,
        email=client.email,
        middle_name=client.middle_name,
        role=client.role,
    )
    payload = {"device_id": generate_device_id}

    return {
        "user": client_entity,
        "payload": payload,
    }


@pytest.mark.django_db
def test_create_access_token(token_service: BaseTokenService, service_params, get_current_timestamp):
    access_token = token_service.create_access_token(**service_params)

    assert token_service.get_token_type_from_token(token=access_token) == TokenType.ACCESS
    assert token_service.get_device_id_from_token(token=access_token) == service_params['payload']['device_id']
    assert token_service.get_client_role_from_token(token=access_token) == service_params['user'].role
    assert token_service.get_client_email_from_token(token=access_token) == service_params['user'].email
    assert token_service.get_expiration_time_from_token(token=access_token) > get_current_timestamp


@pytest.mark.django_db
def test_create_refresh_token(
        token_service: BaseTokenService,
        service_params,
        get_current_timestamp,
):
    refresh_token = token_service.create_refresh_token(**service_params)

    assert token_service.get_token_type_from_token(token=refresh_token) == TokenType.REFRESH
    assert token_service.get_device_id_from_token(token=refresh_token) == service_params['payload']['device_id']
    assert token_service.get_client_role_from_token(token=refresh_token) == service_params['user'].role
    assert token_service.get_client_email_from_token(token=refresh_token) == service_params['user'].email
    assert token_service.get_expiration_time_from_token(token=refresh_token) > get_current_timestamp


@pytest.mark.django_db
def test_get_raw_jwt_payload(token_service: BaseTokenService, service_params):
    access_token = token_service.create_access_token(**service_params)
    payload = token_service.get_raw_jwt(token=access_token)

    assert payload["exp"] == token_service.get_expiration_time_from_token(token=access_token)
    assert payload["type"] == token_service.get_token_type_from_token(token=access_token)
    assert payload["sub"] == service_params['user'].email
    assert payload["client_email"] == service_params['user'].email
    assert payload["client_roles"] == service_params['user'].role
    assert payload["device_id"] == service_params['payload']['device_id']
    assert payload["iat"] <= token_service.get_expiration_time_from_token(token=access_token)
