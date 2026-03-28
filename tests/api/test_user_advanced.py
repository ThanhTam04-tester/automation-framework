import pytest
from api.user_api import UserAPI
from jsonschema import validate
from core.data_loader import load_json


# ===== TEST SCHEMA =====
@pytest.mark.api
def test_get_users_schema(api_client):
    user_api = UserAPI(api_client)

    res = user_api.get_users()
    assert res.status_code == 200

    data = res.json()

    schema = load_json("test_data/api/user_schema.json")

    validate(instance=data, schema=schema)


# ===== TEST CREATE =====
@pytest.mark.api
def test_create_user(api_client):
    user_api = UserAPI(api_client)

    payload = {
        "name": "Tam",
        "job": "Tester"
    }

    response = user_api.create_user(payload)

    assert response.status_code in [200, 201]


# ===== TEST FLOW =====
@pytest.mark.api
def test_user_flow(api_client):
    user_api = UserAPI(api_client)

    # create
    payload = {"name": "Test", "job": "QA"}
    create_res = user_api.create_user(payload)
    assert create_res.status_code in [200, 201]

    # get
    get_res = user_api.get_users()
    assert get_res.status_code == 200