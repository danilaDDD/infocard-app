import pytest
from rest_framework.test import APIClient

from apps.account.models import PrimaryToken


@pytest.fixture(scope="session")
def client() -> APIClient:
    return APIClient()

@pytest.fixture(scope="function")
def primary_token(django_db_blocker) -> PrimaryToken:
    with django_db_blocker.unblock():
        return PrimaryToken.objects.create(token="test)", is_active=True)


