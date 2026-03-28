from api.auth_api import AuthAPI


class FakeResponse:
    def __init__(self, status_code=200, text='{"token": "abc123"}'):
        self.status_code = status_code
        self.text = text


class FakeAPIClient:
    def post(self, endpoint, **kwargs):
        return FakeResponse()


def test_auth_login():
    api_client = FakeAPIClient()
    auth_api = AuthAPI(api_client)

    response = auth_api.login("test_user", "123456")

    assert response.status_code == 200
    assert "token" in response.text