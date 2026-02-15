import pytest

from apps.account.models import Account


@pytest.mark.django_db
class TestAccountCRUD:
    def test_create_account(self):
        acc = Account.objects.create(username="test_user", password="password123", email="test@test.ru")
        assert acc is not None