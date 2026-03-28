from core.api_client import APIClient


class FakeResponse:
    def __init__(self, status_code=200, text='{"message": "success"}'):
        self.status_code = status_code
        self.text = text


def fake_request(self, method, url, headers=None, timeout=None, **kwargs):
    return FakeResponse(status_code=200, text='{"message": "success"}')


def test_api_client_get(monkeypatch):
    monkeypatch.setattr("requests.sessions.Session.request", fake_request)

    client = APIClient(base_url="https://fake-api.com", timeout=10)
    response = client.get("/users")

    assert response.status_code == 200
    assert "success" in response.text


def test_api_client_post(monkeypatch):
    monkeypatch.setattr("requests.sessions.Session.request", fake_request)

    client = APIClient(base_url="https://fake-api.com", timeout=10)
    response = client.post("/auth/login", json={"username": "admin", "password": "123456"})

    assert response.status_code == 200
    assert "success" in response.text