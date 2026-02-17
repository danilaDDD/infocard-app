import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import Account
from apps.common.jwt_utils import check_jwt, TYPE_ACCESS_TOKEN, TYPE_REFRESH_TOKEN
from apps.common.request_generator import gen_valid_registration_request_data

@pytest.mark.django_db
@pytest.mark.e2e
class TestRefreshRequest:
    @pytest.fixture(autouse=True, scope='function')
    def setup(self, client, primary_token):
        self.client = client
        self.primary_token = primary_token
        yield

    def test_when_valid_token_then_return_200(self):
        saved_account = self.create_account()
        valid_refresh_token = RefreshToken.for_user(saved_account)
        req_data = {'refresh': str(valid_refresh_token)}
        resp = self.do_request(req_data,
                               access_token=self.primary_token.token)

        assert resp.status_code == 200

        resp_data = resp.data
        assert check_jwt(resp_data.get('access'), saved_account, type=TYPE_ACCESS_TOKEN)
        assert check_jwt(resp_data.get('refresh'), saved_account, type=TYPE_REFRESH_TOKEN)

    def test_when_invalid_token_then_return_401(self):
        req_data = {'refresh': 'invalid_token'}
        resp = self.do_request(req_data, access_token=self.primary_token.token)

        assert resp.status_code == 401
        assert len(resp.data['detail']) > 0

    @pytest.mark.parametrize("req_data",  [
        {},
        {"refresh": ""},
        {"invalid_field": "value"},
    ])
    def test_when_bad_request_then_return_400(self, req_data):
        self.create_account()
        resp = self.do_request(req_data, access_token=self.primary_token.token)

        assert resp.status_code == 400
        assert len(resp.data['refresh']) > 0

    def test_when_invalid_primary_token_then_return_401(self):
        valid_refresh_token = RefreshToken.for_user(self.create_account())
        req_data = {'refresh': str(valid_refresh_token)}
        resp = self.do_request(req_data, access_token='invalid_primary_token')

        assert resp.status_code == 401
        assert len(resp.data['detail']) > 0

    def test_when_not_existing_account_then_return_401(self):
        valid_refresh_token = RefreshToken.for_user(self.create_account())
        req_data = {'refresh': str(valid_refresh_token)}
        Account.objects.all().delete()
        resp = self.do_request(req_data, access_token=self.primary_token.token)

        assert resp.status_code == 401
        assert len(resp.data['detail']) > 0

    def create_account(self) -> Account:
        account_kwargs = gen_valid_registration_request_data()
        return (Account.objects
                .create_user(**account_kwargs))

    def do_request(self, req_data, access_token):
        return self.client.post(
            '/users/refresh/',
            data=req_data,
            headers={'X-Access-Token': access_token}
        )
