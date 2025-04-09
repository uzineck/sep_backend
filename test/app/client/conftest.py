import pytest
import uuid
from datetime import (
    datetime,
    timezone,
)
from test.factories.client.client import ClientModelFactory

from core.apps.news.services.user import BaseClientService
from core.apps.common.auth.password import BasePasswordService
from core.apps.common.auth.token import BaseTokenService
from core.apps.common.factory import convert_to_timestamp


@pytest.fixture
def client_service(container) -> BaseClientService:
    return container.resolve(BaseClientService)


@pytest.fixture
def password_service(container) -> BasePasswordService:
    return container.resolve(BasePasswordService)


@pytest.fixture
def token_service(container) -> BaseTokenService:
    return container.resolve(BaseTokenService)


@pytest.fixture(scope='function')
def client_create():
    def _client_create(**kwargs):
        return ClientModelFactory.create(**kwargs)

    return _client_create


@pytest.fixture(scope='function')
def client_build():
    def _client_build(**kwargs):
        return ClientModelFactory.build(**kwargs)

    return _client_build


@pytest.fixture
def hash_password(password_service: BasePasswordService):
    def _hash_password(plain_password: str) -> str:
        return password_service.hash_password(plain_password)

    return _hash_password


@pytest.fixture
def generate_email(faker):
    def _generate_email() -> str:
        return f'{faker.user_name()}@gmail.com'

    return _generate_email


@pytest.fixture
def generate_password(faker):
    def _generate_password() -> str:
        return faker.password(length=10)

    return _generate_password


@pytest.fixture
def generate_device_id():
    return str(uuid.uuid4())


@pytest.fixture
def get_current_timestamp():
    return convert_to_timestamp(datetime.now(tz=timezone.utc))
