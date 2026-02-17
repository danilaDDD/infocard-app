import pytest
from rest_framework.response import Response

from apps.account.models import Account
from apps.common.asserts import assert_error_response
from apps.common.jwt_utils import check_jwt, TYPE_ACCESS_TOKEN, TYPE_REFRESH_TOKEN
from apps.common.request_generator import gen_valid_registration_request_data


@pytest.mark.django_db
@pytest.mark.e2e
class TestLoginRequest:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, client, primary_token):
        self.client = client
        self.primary_token = primary_token
        yield

    def test_when_valid_request_then_return_200(self):
        auth_req = {'username': 'test_user', 'password': 'password123'}
        saved_account = self.create_account(**auth_req)

        resp = self.do_request(auth_req, access_token=self.primary_token.token)

        assert resp.status_code == 200
        resp_data = resp.data
        assert check_jwt(resp_data.get('access'), saved_account, type=TYPE_ACCESS_TOKEN)
        assert check_jwt(resp_data.get('refresh'), saved_account, type=TYPE_REFRESH_TOKEN)

    @pytest.mark.parametrize("auth_req", [
        {'username': 'test_user', 'password': 'wrong_password'},
        {'username': 'wrong_user', 'password': 'password123'},
    ])
    def test_when_invalid_login_then_return_401(self, auth_req):
        self.create_account(username='test_user', password='password123')

        resp = self.do_request(auth_req, access_token=self.primary_token.token)
        assert_error_response(resp, 401)

    @pytest.mark.parametrize("req_data", [
        {"username": "", "password":"password123"},
        {"username": "test_user", "password": ""},
        {"username": "", "password": ""},
        {"username": "test_user"},
        {"password": "password123"},
        {"invalid_field": "value"},
    ])
    def test_when_invalid_access_token_then_return_401(self, req_data: dict):
        auth_req = {'username': 'test_user', 'password': 'password123'}
        self.create_account(**auth_req)

        resp = self.do_request(auth_req, access_token='invalid_token')
        assert_error_response(resp, 401)

    def do_request(self, auth_req: dict, access_token: str) -> 'Response':
        return self.client.post(
            '/users/login/',
            data=auth_req,
            headers={'X-Access-Token': access_token}
        )

    def create_account(self, username: str, password: str) -> Account:
        account_kwargs = gen_valid_registration_request_data(username=username, password=password)
        return (Account.objects
                .create_user(**account_kwargs))