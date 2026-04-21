from faker import Faker
from sqlmodel import Session
from app.crud.library import ServicioBiblioteca as crud
from app.crud.books import ServicioLibros
from app.crud.users import ServicioUsuario
from app.models.estanteria import Estanteria
from app.models.books import LibroCrear, LibroFiltro


def test_add_book_to_favoritos(session: Session) -> None:
    nombre_estanteria = "favoritos"
  
    fake = Faker()
    name = "Harry Potter"
    book = LibroCrear(
        nombre=name,
        isbn=fake.isbn10(),
        fecha_publicacion=fake.date(),
        descripcion="Magia",
        generos=["fantasia"],
        id_autor=2)

    ServicioLibros.create_book(session=session, book_create=book)
    
    books = ServicioLibros.get_books(session=session, book_filter=LibroFiltro())
    book = books[0]
    
    users = ServicioUsuario.get_users(session=session)
    user = users[0]

    estanteria = crud.add_book(session=session, current_user=user, nombre_estanteria=nombre_estanteria, id_libro=book.id)

    assert estanteria is not None
    assert estanteria.nombre == nombre_estanteria
    assert len(estanteria.libros) > 0
    assert estanteria.libros[0].nombre == book.nombre  