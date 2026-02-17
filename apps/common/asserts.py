from rest_framework.response import Response


def assert_error_response(response: Response, status_code=400):
    assert response.status_code == status_code
    resp_data = response.data
    assert len(resp_data) > 0