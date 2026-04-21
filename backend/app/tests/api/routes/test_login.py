from faker import Faker
from fastapi.testclient import TestClient


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": "bob@company.com",
        "password": "valid-passw0rd",
    }

    r = client.post("/login/access-token", data=login_data)

    tokens = r.json()

    print(tokens)

    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": "bob@company.com",
        "password": "incorrect",
    }
    
    r = client.post("/login/access-token", data=login_data)

    assert r.status_code == 400

def test_get_access_token_user_not_exists(client: TestClient) -> None:
    login_data = {
        "username": "not_a_real_user@fake.com",
        "password": "whatever"
    }

    r = client.post("/login/access-token", data=login_data)

    assert r.status_code == 400