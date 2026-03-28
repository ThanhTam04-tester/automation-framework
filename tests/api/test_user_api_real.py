from core.api_client import APIClient
from api.user_api import UserAPI


def test_get_users_real():
    client = APIClient(base_url="https://jsonplaceholder.typicode.com")
    user_api = UserAPI(client)

    response = user_api.get_users()

    assert response.status_code == 200