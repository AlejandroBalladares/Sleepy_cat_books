from faker import Faker
from fastapi.testclient import TestClient
from app.models.comunidad import TipoComunidad

Faker.seed(0)
fake = Faker()

def test_get_communities(client: TestClient) -> None:
    response = client.get("/communities") 
    assert response.status_code == 200 
    
    communities = response.json()
    
    expected_communities = [
        {
            "nombre": "Lectores de Ciencia Ficción",
            "descripcion": "Comunidad para los amantes de la ciencia ficción",
            "id_creador": 1
        },
        {
            "nombre": "Lectores de Romance",
            "descripcion": "Comunidad para los amantes de las historias de amor",
            "id_creador": 2
        }
    ]
    
    for community, expected in zip(communities, expected_communities):
        assert community["nombre"] == expected["nombre"]
        assert community["descripcion"] == expected["descripcion"]
        assert community["id_creador"] == expected["id_creador"]


def test_get_communities_by_name(client: TestClient) -> None:
    name = "Lectores de Misterio"
    response = client.get(
        url="/communities",
        params={"name": name}
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()
    
    assert isinstance(data, list)
    for comunidad in data:
        assert name.lower() in comunidad["nombre"].lower()

def test_get_community_invalid_id(client: TestClient) -> None:
    community_id = -1 
    response = client.get(
        url=f"/communities/{community_id}"
    )

    assert response.status_code == 404

# Lectores y Autores pueden crear comunidades
def test_create_community_success(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "nombre": fake.company(),
        "imagen": "imagen.jpg",
        "tipo": TipoComunidad.PUBLICO,
        "descripcion": fake.text(max_nb_chars=100)
    }
    
    response = client.post(
        url="/communities",
        json=data,
        headers=reader_token_headers
    )

    assert response is not None
    assert response.status_code == 200

    data_response = response.json()
    assert data_response["nombre"] == data["nombre"]
    assert data_response["tipo"] == data["tipo"]

def test_create_community_not_logged_in(client: TestClient) -> None:
    data = {
        "nombre": fake.company(),
        "imagen": "http://imagen.com/imagen.jpg",
        "tipo": TipoComunidad.PUBLICO.value,
        "descripcion": fake.text(max_nb_chars=100)
    }
    
    response = client.post(
        url="/communities",
        json=data
    )

    assert response is not None
    assert response.status_code == 401

def test_edit_community(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    
    # Comunidad Original
    data_create = {
        "nombre": fake.company(),
        "tipo": TipoComunidad.PUBLICO.value,
        "descripcion": fake.text(max_nb_chars=100),
        "imagen": "http://imagen.com/original.jpg",
    }

    create_response = client.post(
        url="/communities",
        json=data_create,
        headers=reader_token_headers
    )

    community = create_response.json()
    community_id = community["id"]

    # Comunidad Editada
    data_edit = {
        "nombre": fake.company(),
        "tipo": TipoComunidad.PRIVADO.value,
        "descripcion": fake.text(max_nb_chars=50),
        "imagen": "http://imagen.com/updated.jpg"
    }

    response = client.patch(
        url=f"/communities/{community_id}",
        json=data_edit,
        headers=reader_token_headers
    )

    assert response.status_code == 200
    edited_community = response.json()

    # Verificar que los cambios se aplicaron correctamente
    assert edited_community["nombre"] == data_edit["nombre"]
    assert edited_community["tipo"] == data_edit["tipo"]
    assert edited_community["descripcion"] == data_edit["descripcion"]
    assert edited_community["imagen"] == data_edit["imagen"]
    
    # Verificar que los campos no modificados permanecen iguales
    assert edited_community["id"] == community_id
    assert edited_community["id_creador"] is not None

def test_edit_community_not_owner(client: TestClient, author_token_headers: dict[str, str]) -> None:
    community_id = 2
    data_edit = {
        "descripcion": "Una nueva descripcion para la comunidad",
    }

    response = client.patch(
        url=f"/communities/{community_id}",
        json=data_edit,
        headers=author_token_headers
    )
    
    assert response is not None
    assert response.status_code == 401

def test_community_add_member(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 1

    response = client.post(
        url=f"/communities/{community_id}/members",
        json={},
        headers=reader_token_headers
    )

    assert response is not None
    assert response.status_code == 200

    community = response.json()

    assert community["id"] == community_id
    assert community["id_creador"] == 1

    user_id = 2 # Reader id
    response = client.get(
        url=f"/communities/{community_id}/members"
    )

    assert response is not None
    assert response.status_code == 200

    members = response.json()

    assert any(user_id == member["id"] for member in members)


def test_community_add_member_already_exist(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 1

    response = client.post(
        url=f"/communities/{community_id}/members",
        json={},
        headers=reader_token_headers
    )

    assert response is not None
    assert response.status_code == 400


def test_community_not_exists(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 10000

    response = client.post(
        url=f"/communities/{community_id}/members",
        json={},
        headers=reader_token_headers
    )

    assert response is not None
    assert response.status_code == 404

def test_community_add_member_creator_fails(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 2

    response = client.post(
        url=f"/communities/{community_id}/members",
        json={},
        headers=reader_token_headers
    )

    assert response is not None
    assert response.status_code == 400
    
def test_community_add_post_is_member(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 1
    user_id = 2
    
    texto_publicacion = fake.text(max_nb_chars=100)
    
    data = {
        "contenido": texto_publicacion,
        "imagenes": ["imagen_1", "imagen_2"]
    }
    
    response = client.post(
        url=f"/communities/{community_id}/posts",
        json=data,
        headers=reader_token_headers
    )
    
    assert response is not None
    assert response.status_code == 200 
    
    response_json = response.json()

    assert response_json["id_usuario"] == user_id
    assert response_json["id_comunidad"] == community_id
    assert response_json["contenido"] == texto_publicacion
    
def test_community_add_post_is_not_member(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 3
    
    texto_publicacion = fake.text(max_nb_chars=100)
    
    data = {
        "contenido": texto_publicacion,
        "imagenes": ["imagen_1", "imagen_2"]
    }
    
    response = client.post(
        url=f"/communities/{community_id}/posts",
        json=data,
        headers=reader_token_headers
    )
    
    assert response is not None
    assert response.status_code == 403 
    
def test_community_with_posts_get_posts(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 1
    
    response = client.get(
        url=f"/communities/{community_id}/posts",
        headers=reader_token_headers
    )
    
    assert response is not None
    assert response.status_code == 200 
    
    response_json = response.json()

    assert len(response_json) == 1
    
def test_community_with_zero_posts_get_posts(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    community_id = 3
    
    response = client.get(
        url=f"/communities/{community_id}/posts",
        headers=reader_token_headers
    )
    
    assert response is not None
    assert response.status_code == 200 
    
    response_json = response.json()

    assert len(response_json) == 0