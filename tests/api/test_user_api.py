import pytest

@pytest.mark.api
def test_get_users(api_client):
    response = api_client.get("/users")

    assert response.status_code == 200