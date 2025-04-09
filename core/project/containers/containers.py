from functools import lru_cache

import punq

from core.project.containers.client import register_client_services
from core.project.containers.validators import register_validators


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    register_client_services(container=container)

    register_validators(container=container)
    return container

