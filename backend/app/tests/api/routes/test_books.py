from faker import Faker
from fastapi.testclient import TestClient

Faker.seed(0)
fake = Faker()


def test_get_books_by_genre(client: TestClient) -> None:
    genre = "fantasia"
    response = client.get(
        url="/books",
        params={"genre": genre}
    )

    assert response is not None
    assert response.status_code == 200
    
    data = response.json()

    assert len(data) == 2
    
    for libro in data:
        for genero in libro["generos"]:
            assert genero["nombre"] == genre


def test_get_book_genre_not_exist(client: TestClient) -> None:
    genre = "no existe"
    response = client.get(
        url="/books",
        params={"genre": genre}
    )

    assert response is not None
    assert response.status_code == 200
    
    data = response.json()

    assert len(data) == 0

def test_get_book_by_name(client: TestClient) -> None:
    title = "sherlock"

    response = client.get(
        url="/books",
        params={"title": title}
    )

    assert response is not None
    assert response.status_code == 200
    
    data = response.json()

    assert len(data) == 1
    assert data[0]["nombre"].lower().find(title)

def test_get_book_by_name_not_exist(client: TestClient) -> None:
    title = "not a book"

    response = client.get(
        url="/books",
        params={"title": title}
    )

    assert response is not None
    assert response.status_code == 200
    
    data = response.json()

    assert len(data) == 0

def test_get_book_by_author_name(client: TestClient) -> None:
    author_name = "bob"
    
    response = client.get(
        url="/books",
        params={"author_name": author_name}
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

def test_get_book_by_author_surname(client: TestClient) -> None:
    author_surname = "robinson"
    
    response = client.get(
        url="/books",
        params={"author_surname": author_surname}
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

def test_get_book_by_author_name_and_surname(client: TestClient) -> None:
    author_name = "bob"
    author_surname = "robinson"

    response = client.get(
        url="/books",
        params={"author_name": author_name, "author_surname": author_surname}
    )
    
    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

def test_get_genres(client: TestClient) -> None:
    response = client.get(
        url="/books/generos",
    )

    assert response is not None
    assert response.status_code == 200

    genres = response.json()

    assert len(genres) > 0

    for genre in genres:
        assert "id" in genre
        assert "nombre" in genre

def test_create_book_success(client: TestClient, author_token_headers: dict[str, str]) -> None:
    name = fake.name()
    isbn = fake.isbn10("")

    data = {
        "nombre": name,
        "isbn": isbn,
        "fecha_publicacion": fake.date(),
        "descripcion": fake.text(max_nb_chars=100),
        "portada": "http://portada.com",
        "generos": [
            "fantasia",
            "romance"
        ]
    }
    
    response = client.post(
        url="/books",
        json=data,
        headers=author_token_headers
    )

    assert response is not None
    assert response.status_code == 200
    data = response.json()

    assert data["nombre"] == name
    assert data["isbn"] == isbn

def test_create_book_not_loggin(client: TestClient) -> None:
    data = {
        "nombre": fake.name(),
        "isbn": fake.isbn10(""),
        "fecha_publicacion": fake.date(),
        "descripcion": fake.text(max_nb_chars=100),
        "portada": "http://portada.com",
        "generos": [
            "fantasia",
            "romance"
        ]
    }
    
    response = client.post(
        url="/books",
        json=data,
    )

    assert response is not None
    assert response.status_code == 401


def test_create_book_not_author(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "nombre": fake.name(),
        "isbn": fake.isbn10(""),
        "fecha_publicacion": fake.date(),
        "descripcion": fake.text(max_nb_chars=100),
        "portada": "http://portada.com",
        "generos": [
            "fantasia",
            "romance"
        ]
    }
    
    response = client.post(
        url="/books",
        headers=reader_token_headers,
        json=data,
    )

    assert response is not None
    assert response.status_code == 401

def test_create_book_duplicate_isbn(client: TestClient, author_token_headers: dict[str, str]) -> None:
    name = fake.name()
    isbn = fake.isbn10("")

    data = {
        "nombre": name,
        "isbn": isbn,
        "fecha_publicacion": fake.date(),
        "descripcion": fake.text(max_nb_chars=100),
        "portada": "http://portada.com",
        "generos": [
            "fantasia",
            "romance"
        ]
    }
    
    _ = client.post(
        url="/books",
        json=data,
        headers=author_token_headers
    )


    response = client.post(
        url="/books",
        json=data,
        headers=author_token_headers
    )

    assert response.status_code == 400
    

def test_create_review(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "contenido": fake.text(max_nb_chars=100)
    }

    id_libro = 1

    response = client.post(
        url=f"/books/{id_libro}/reviews",
        headers=reader_token_headers,
        json=data
    )
    
    assert response is not None
    assert response.status_code == 200
    assert response.json()["id_libro"] == id_libro


def test_create_review_invalid_book(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "contenido": fake.text(max_nb_chars=100)
    }

    id_libro = 100

    response = client.post(
        url=f"/books/{id_libro}/reviews",
        headers=reader_token_headers,
        json=data
    )
    
    assert response.status_code == 404
    
def test_create_review_already_exists(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "contenido": fake.text(max_nb_chars=100)
    }

    id_libro = 1

    response = client.post(
        url=f"/books/{id_libro}/reviews",
        headers=reader_token_headers,
        json=data
    )
    
    assert response.status_code == 400

def test_get_reviews(client: TestClient) -> None:
    id_libro = 1
    
    response = client.get(
        url=f"/books/{id_libro}/reviews"
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3


def test_get_book_by_id(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    id_libro = 1
    
    response = client.get(
        url=f"/books/{id_libro}"
    )
    
    assert response is not None
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["id"] == id_libro
    
def test_get_book_by_wrong_id(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    id_libro = 66666
    
    response = client.get(
        url=f"/books/{id_libro}"
    )
    
    assert response is not None
    assert response.status_code == 404
    
def test_create_rating(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "puntuacion": 1
    }

    id_libro = 1

    response = client.post(
        url=f"/books/{id_libro}/ratings",
        headers=reader_token_headers,
        json=data
    )
    
    assert response is not None
    assert response.status_code == 200
    assert response.json()["id_libro"] == id_libro


def test_create_rating_invalid_book(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "puntuacion": fake.random_int(min=1, max=5)
    }

    id_libro = 100

    response = client.post(
        url=f"/books/{id_libro}/ratings",
        headers=reader_token_headers,
        json=data
    )
    
    assert response.status_code == 404
    
def test_create_rating_already_exists(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "puntuacion": fake.random_int(min=1, max=5)
    }

    id_libro = 1

    response = client.post(
        url=f"/books/{id_libro}/ratings",
        headers=reader_token_headers,
        json=data
    )
    
    assert response.status_code == 400

def test_get_ratings(client: TestClient) -> None:
    id_libro = 1
    
    response = client.get(
        url=f"/books/{id_libro}/ratings"
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1

def test_update_rating(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    data = {
        "puntuacion": 5
    }

    id_libro = 1

    response = client.patch(
        url=f"/books/{id_libro}/ratings",
        headers=reader_token_headers,
        json=data
    )
    
    assert response is not None
    assert response.status_code == 200
    
    data = response.json()
    
    assert data['puntuacion'] == 5
    
def test_delete_rating(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    id_libro = 1

    response = client.delete(
        url=f"/books/{id_libro}/ratings",
        headers=reader_token_headers
    )
    
    assert response is not None
    assert response.status_code == 200

def test_update_book(client: TestClient, author_token_headers: dict[str,str]) -> None:
    id_libro = 3
    new_name = "Memorias de una Geisha"
    new_description = "Historia de una Geisha que trabajaba en Kioto antes de la Segunda Guerra Mundial"
    new_cover = "https://otraportadadememoriasdeunageisha.com"

    body = {
        "nombre": new_name,
        "descripcion": new_description,
        "portada": new_cover,
        "imagenes_ilustrativas": [
            "https://imagenilustrativa-1.com",
            "https://imagenilustrativa-2.com",
            "https://imagenilustrativa-3.com"
        ]
    }
    
    response = client.patch(
        url=f"/books/{id_libro}",
        headers=author_token_headers,
        json=body
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == id_libro
    assert data["nombre"] == new_name
    assert data["descripcion"] == new_description
    assert data["portada"] == new_cover
    assert len(data["imagenes_ilustrativas"]) == 3

def test_update_book_not_author(client: TestClient, reader_token_headers: dict[str, str]) -> None:
    id_libro = 1

    new_name = "harry potter"
    new_description = "Magia, magia y magia"
    new_cover = "https://otraportadadeharrypotter.com"


    body = {
        "nombre": new_name,
        "descripcion": new_description,
        "portada": new_cover,
        "imagenes_ilustrativas": [
            "https://imagenilustrativa-1.com",
            "https://imagenilustrativa-2.com",
            "https://imagenilustrativa-3.com"
        ]
    }
    
    response = client.patch(
        url=f"/books/{id_libro}",
        headers=reader_token_headers,
        json=body
    )

    assert response is not None
    assert response.status_code == 401

def test_update_book_not_author_of_book(client: TestClient, author_token_headers: dict[str, str]) -> None:
    id_libro = 2

    new_name = "The Little Prince"
    new_description = "And now here is my secret, a very simple secret: It is only with the heart that one can see rightly; what is essential is invisible to the eye."
    new_cover = "https://otraportadadeharrypotter.com"


    body = {
        "nombre": new_name,
        "descripcion": new_description,
        "portada": new_cover,
        "imagenes_ilustrativas": [
            "https://imagenilustrativa-1.com",
            "https://imagenilustrativa-2.com",
            "https://imagenilustrativa-3.com"
        ]
    }
    
    response = client.patch(
        url=f"/books/{id_libro}",
        headers=author_token_headers,
        json=body
    )

    assert response is not None
    assert response.status_code == 403

def test_update_book_empty_imagenes_ilustrativas(client: TestClient, author_token_headers: dict[str, str]) -> None:
    id_libro = 3

    body = {
        "imagenes_ilustrativas": []
    }
    
    response = client.patch(
        url=f"/books/{id_libro}",
        headers=author_token_headers,
        json=body
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == id_libro
    assert len(data["nombre"]) > 0
    assert len(data["descripcion"]) > 0
    assert len(data["portada"]) > 0
    assert len(data["imagenes_ilustrativas"]) == 0

def test_update_book_None_imagenes_ilustrativas_ignored(client: TestClient, author_token_headers: dict[str, str]) -> None:
    id_libro = 3

    body = {
        "imagenes_ilustrativas": [None]
    }
    
    response = client.patch(
        url=f"/books/{id_libro}",
        headers=author_token_headers,
        json=body
    )

    assert response is not None
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == id_libro
    assert len(data["nombre"]) > 0
    assert len(data["descripcion"]) > 0
    assert len(data["portada"]) > 0
    assert len(data["imagenes_ilustrativas"]) == 0