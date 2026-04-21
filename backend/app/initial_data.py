import logging

from sqlmodel import Session, select
from app.models.users import Usuario
from app.models.books import Genero, Libro, Reseña
from app.models.comunidad import Comunidad, Publicacion
from app.crud.users import ServicioUsuario
from app.db_seed import seed_generos, seed_usuarios, seed_libros, seed_reseñas, seed_comunidades, seed_posts

from app.core.db import engine
from app.crud.books import ServicioLibros
from app.crud.comunidad import ServicioComunidad

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(session: Session) -> None:
    usuarios = [usuario.nombre_de_usuario for usuario in session.exec(select(Usuario)).all()]

    for usuario in seed_usuarios:
        if usuario.nombre_de_usuario not in usuarios:
            ServicioUsuario.create_user(session=session, user_create=usuario)
        
    generos = [genero.nombre for genero in session.exec(select(Genero)).all()]

    for genero in seed_generos:
        if genero not in generos:
            session.add(Genero(nombre=genero))
            session.commit()

    libros = [libros.isbn for libros in session.exec(select(Libro)).all()]

    for libro in seed_libros:
        if libro.isbn not in libros:
            ServicioLibros.create_book(session=session, book_create=libro)

    comunidades = [comunidad.nombre for comunidad in session.exec(select(Comunidad)).all()]

    for comunidad in seed_comunidades:
        if comunidad.nombre not in comunidades:
            ServicioComunidad.create_community(session=session, community_create=comunidad)
            
    for reseña in seed_reseñas:
        if session.exec(select(Reseña).where(Reseña.id_libro == reseña.id_libro, Reseña.id_usuario == reseña.id_usuario)).first() is None:
            session.add(reseña)
            session.commit()

    for post in seed_posts:
        if session.exec(select(Publicacion).where(Publicacion.id_comunidad == post.id_comunidad, Publicacion.id_usuario == post.id_usuario)).first() is None:
            session.add(post)
            session.commit()

def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()