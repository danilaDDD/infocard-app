import pytest
from rest_framework.response import Response

from apps.account.models import Account
from apps.common.asserts import assert_error_response
from apps.common.jwt_utils import TYPE_ACCESS_TOKEN, check_jwt, TYPE_REFRESH_TOKEN
from apps.common.request_generator import gen_valid_registration_request_data, gen_invalid_registration_request_data


@pytest.mark.django_db
@pytest.mark.e2e
class TestRegistrationRequest:
    @pytest.fixture(autouse=True)
    def setup(self, client, primary_token):
        self.client = client
        self.primary_token = primary_token
        yield

    @pytest.mark.parametrize(
        "request_data",
            [
                gen_valid_registration_request_data(),
                gen_valid_registration_request_data(gender=Account.MALE_GENDER),
                gen_valid_registration_request_data(telegram_id=1232336343),
        ],
    )
    def test_when_valid_request_then_return_200_and_saved(self, request_data: dict):
        resp = self.do_request(request_data, access_token=self.primary_token.token)

        assert resp.status_code == 201
        resp_data = resp.data

        user = resp_data.get("user")
        assert user is not None
        assert user.get("id") > 0

        tokens = resp_data.get("tokens")
        assert tokens is not None

        accounts = Account.objects.all()
        assert len(accounts) == 1
        account = accounts[0]

        assert check_jwt(tokens.get("access"), account, type=TYPE_ACCESS_TOKEN)
        assert check_jwt(tokens.get("refresh"), account, type=TYPE_REFRESH_TOKEN)

    def test_when_invalid_access_token_then_return_401(self):
        valid_resp_data = gen_valid_registration_request_data()
        resp = self.do_request(valid_resp_data, access_token="invalid_token")

        assert_error_response(resp, 401)

    @pytest.mark.parametrize("request_data",
        gen_invalid_registration_request_data()
    )
    def test_when_invalid_response_data_then_return_400(self, request_data: dict):
        resp = self.do_request(request_data, access_token=self.primary_token.token)
        assert_error_response(resp, 400)

    def do_request(self, request_data, access_token=None) -> Response:

        return self.client.post(
            "/users/",
            headers={"X-Access-Token": access_token} if access_token is not None else {},
            data=request_data,
        )

