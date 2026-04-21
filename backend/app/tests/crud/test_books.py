from faker import Faker
from sqlmodel import Session
from app.crud.books import ServicioLibros as crud
from app.models.books import LibroCrear, LibroFiltro


def test_create_book(session: Session) -> None:
    fake = Faker()

    name = "Harry Potter"

    book = LibroCrear(
        nombre=name,
        isbn=fake.isbn10(),
        fecha_publicacion=fake.date(),
        descripcion="Magia",
        generos=["fantasia"],
        id_autor=2)

    crud.create_book(session=session, book_create=book)
    result = crud.get_books(session=session, book_filter=LibroFiltro(title=name))

    assert result is not None
    assert result[0].nombre == name