from fastapi.testclient import TestClient


def get_user_token_header(client: TestClient, login_data: dict[str, str]) -> dict[str, str]:
    response = client.post(
        "/login/access-token",
        data=login_data
    )

    token = response.json()['access_token']

    return {"Authorization": f"Bearer {token}"}

def get_author_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": "bob@company.com",
        "password": "valid-passw0rd",
    }

    return get_user_token_header(client, login_data)

def get_reader_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": "alice@company.com",
        "password": "valid-passw0rd",
    }

    return get_user_token_header(client, login_data)
