from fastapi.testclient import TestClient
from sqlmodel import Session
from faker import Faker
from app.crud.users import ServicioUsuario as crud

def test_create_user_new_email(client: TestClient, session: Session) -> None:
    data = {
        "contraseña": Faker().password(),
        "email": Faker().email(),
        "nombre": "Bob",
        "apellido": "Robinson",
        "nombre_de_usuario": Faker().user_name(),
        "fecha_nacimiento": "1979-04-20",
        "rol": "LECTOR"
    }
    
    response = client.post(
        "/users/signup",
        json=data,
    )

    assert 200 <= response.status_code < 300
    created_user = response.json()
    user = crud.get_user_by_email(session=session, email=data['email'])
    assert user
    assert user.email == created_user["email"]
    
def test_create_user_used_email(client: TestClient, session: Session) -> None:
    data = {
        "contraseña": Faker().password(),
        "email": Faker().email(),
        "nombre": "Bob",
        "apellido": "Robinson",
        "nombre_de_usuario": Faker().user_name(),
        "fecha_nacimiento": "1979-04-20",
        "rol": "LECTOR"
    }
    
    client.post(
        "/users/signup",
        json=data,
    )
    
    data["nombre_de_usuario"] = Faker().user_name()
    response = client.post(
        "/users/signup",
        json=data,
    )

    assert response.status_code == 400

def test_create_user_short_password(client: TestClient, session: Session) -> None:
    data = {
        "contraseña": "short",
        "email": Faker().email(),
        "nombre": "Bob",
        "apellido": "Robinson",
        "nombre_de_usuario": Faker().user_name(),
        "fecha_nacimiento": "1979-04-20",
        "rol": "LECTOR"
    }

    response = client.post(
        "/users/signup",
        json=data,
    )

    assert response.status_code == 400


def test_get_me(client: TestClient, author_token_headers: dict[str, str]) -> None:
    response = client.get(
        "/users/me",
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert data["nombre"] == "Bob"
    assert data["apellido"] == "Robinson"
    assert data["email"] == "bob@company.com"
    
def test_update_me_add_pic_and_description(client: TestClient, author_token_headers: dict[str, str]) -> None:
    foto_de_perfil = Faker().image_url()
    descripcion = Faker().sentence()
    
    data = {
        "foto_de_perfil": foto_de_perfil,
        "descripcion": descripcion
    }
        
    response = client.patch(
        "/users/me",
        headers=author_token_headers,
        json=data
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert data["nombre"] == "Bob"
    assert data["apellido"] == "Robinson"
    assert data["email"] == "bob@company.com"
    assert data["descripcion"] == descripcion
    assert data["foto_de_perfil"] == foto_de_perfil
    
def test_update_me_with_same_email(client: TestClient, author_token_headers: dict[str, str]) -> None:
    data = {
        "email": "bob@company.com"
    }
        
    response = client.patch(
        "/users/me",
        headers=author_token_headers,
        json=data
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert data["nombre"] == "Bob"
    assert data["apellido"] == "Robinson"
    assert data["email"] == "bob@company.com"  
    
def test_update_me_with_non_unique_email(client: TestClient, author_token_headers: dict[str, str]) -> None:
    data = {
        "email": "alice@company.com"
    }
        
    response = client.patch(
        "/users/me",
        headers=author_token_headers,
        json=data
    )

    assert response is not None
    assert response.status_code == 400
