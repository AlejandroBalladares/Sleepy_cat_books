from faker import Faker
from fastapi.testclient import TestClient

Faker.seed(0)
fake = Faker()


def test_add_book_to_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    data = {
        "id_libro": 1
    }

    response = client.post(
        url=f"/library/{shelf_name}",
        json=data,
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 200
    
    resp_json = response.json()

    assert resp_json["nombre"] == shelf_name
    
def test_add_book_to_shelf_duplicate(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    data = {
        "id_libro": 1
    }

    response = client.post(
        url=f"/library/{shelf_name}",
        json=data,
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 409
    

def test_add_book_to_unknown_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "unknown"
    data = {
        "id_libro": 1
    }

    response = client.post(
        url=f"/library/{shelf_name}",
        json=data,
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 404
    
def test_add_book_to_shelf_wrong_book_id(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    data = {
        "id_libro": 10000000
    }

    response = client.post(
        url=f"/library/{shelf_name}",
        json=data,
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 404
    

def test_get_books_from_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"

    response = client.get(
        url=f"/library/{shelf_name}",
        headers=author_token_headers
    )  

    assert response is not None
    
    response_json = response.json()

    assert response_json[0]["id"] == 1


def test_get_books_from_unknown_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "unknown"

    response = client.get(
        url=f"/library/{shelf_name}",
        headers=author_token_headers
    )  
    
    assert response is not None    
    assert response.status_code == 404

def test_remove_book_from_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    id_libro = 1
    
    response = client.delete(
        url=f"/library/{shelf_name}/{id_libro}",
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 200

    resp_json = response.json()

    assert resp_json["id"] == id_libro

def test_remove_book_from_unknown_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "unknown"
    id_libro = 1
    
    response = client.delete(
        url=f"/library/{shelf_name}/{id_libro}",
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 404


def test_remove_book_from_shelf_wrong_book_id(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    id_libro = 1000000
    
    response = client.delete(
        url=f"/library/{shelf_name}/{id_libro}",
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 404

def test_remove_book_from_shelf_not_in_shelf(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    id_libro = 2

    response = client.delete(
        url=f"/library/{shelf_name}/{id_libro}",
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 404
    
def test_get_shelves(client: TestClient, author_token_headers: dict[str, str]) -> None:
    shelf_name = "favoritos"
    id_libro = 2

    response = client.get(
        url=f"/library",
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 200
    
    response_json = response.json()
        
    assert 'favoritos' in [estanteria['nombre'] for estanteria in response_json]