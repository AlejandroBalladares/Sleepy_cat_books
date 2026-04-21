from fastapi import HTTPException
from sqlalchemy import Sequence, func
from sqlmodel import Session, or_, select
from app.models.books import ImagenIlustrativa, Libro, LibroCrear, Genero, LibroActualizar, LibroFiltro, Reseña, ReseñaCrear, ReseñaPublico, Puntuacion, PuntuacionCrear, PuntuacionPublico

from app.models.users import Usuario

class ServicioLibros(object):
    def create_book(*, session: Session, book_create: LibroCrear) -> Libro:
        generos = [session.exec(select(Genero).where(Genero.nombre == genero)).first() for genero in book_create.generos]     
        
        if session.exec(select(Libro).where(Libro.isbn == book_create.isbn)).first() is not None:
            raise HTTPException(status_code=400, detail="ISBN ya existe")
        
        db_obj = Libro.model_validate(
            book_create,
            update={"generos":generos}
        )

        print(db_obj)
        
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj
        

    def get_books(session: Session, book_filter: LibroFiltro) -> Sequence[Libro]:
        query = select(Libro)
        author_join = False

        if book_filter.title is not None:
            query = query.where(Libro.nombre.ilike(f"%{book_filter.title}%"))

        if book_filter.genre is not None:
            query = query.join(Libro.generos).where(Genero.nombre == book_filter.genre)

        if book_filter.author_name is not None:
            query = query.join(Usuario).where(Libro.id_autor == Usuario.id, Usuario.nombre.ilike(f"%{book_filter.author_name}%"))
            author_join = True

        if book_filter.author_surname is not None:
            if not author_join:
                query = query.join(Usuario).where(Libro.id_autor == Usuario.id)

            query = query.where(Usuario.apellido.ilike(f"%{book_filter.author_surname}%"))

        libros = session.exec(query).all()
        return libros

    def edit_book(session: Session, current_user: Usuario, book_id: int, book_edit: LibroActualizar) -> Libro:
        book = session.exec(select(Libro).where(Libro.id == book_id, Libro.id_autor == current_user.id)).first()

        if not book:
            raise HTTPException(status_code=403, detail="Usuario no tiene permiso para editar este libro")
        
        book_data = book_edit.model_dump(exclude_unset=True)
        book.sqlmodel_update(book_data)
        if book_edit.imagenes_ilustrativas is not None:
            book.imagenes_ilustrativas = [ImagenIlustrativa(url=url) for url in book_edit.imagenes_ilustrativas if url is not None]
        
        session.add(book)
        session.commit()
        session.refresh(book)
        
        return book
    
    def get_popular_books(session: Session) -> Sequence[Libro]:
        return session.exec(select(Libro)
                            .join(Puntuacion, Libro.id == Puntuacion.id_libro)
                            .join(Reseña, Libro.id == Reseña.id_libro, isouter=True)
                            .group_by(Libro.id)
                            .order_by(func.avg(Puntuacion.puntuacion).desc())
                            .order_by(func.count(Reseña.id_usuario).desc())
                            .order_by(Libro.nombre)
                            ).all()

    def get_generos(session: Session) -> Sequence[Genero]:
        generos = session.exec(select(Genero)).all()
        return generos

    def create_review(session: Session, current_user: Usuario, id_libro: int, review: ReseñaCrear) -> Reseña:
        book = session.exec(select(Libro).where(Libro.id == id_libro)).first()
        
        if book is None:
            raise HTTPException(status_code=404, detail="No existe libro con ese id")
        
        if session.exec(select(Reseña).where(Reseña.id_libro == id_libro, Reseña.id_usuario == current_user.id)).first() is not None:
            raise HTTPException(status_code=400, detail="Ya existe una reseña para este usuario y este libro")
        
        db_obj = Reseña.model_validate(
            review, update={"id_libro": id_libro, "id_usuario": current_user.id}
        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj
    
    def get_reviews(session: Session, id_libro: int) -> list[ReseñaPublico]:
        reviews = session.exec(select(Reseña).where(Reseña.id_libro == id_libro)).all()

        # Is there a better, optimized way to do this?
        return [ReseñaPublico(contenido=review.contenido,
                            id_libro=review.id_libro,
                            usuario=session.exec(select(Usuario).where(Usuario.id == review.id_usuario)).first())
                            for review in reviews]

    def get_book(session: Session, id_libro: int) -> Libro:
        book = session.exec(select(Libro).where(Libro.id == id_libro)).first()
        
        if book is None:
            raise HTTPException(status_code=404, detail="No existe libro con ese id")
        
        return book
    
    def create_rating(session: Session, current_user: Usuario, id_libro: int, rating: PuntuacionCrear) -> Puntuacion:
        book = session.exec(select(Libro).where(Libro.id == id_libro)).first()
        
        if book is None:
            raise HTTPException(status_code=404, detail="No existe libro con ese id")
        
        if session.exec(select(Puntuacion).where(Puntuacion.id_libro == id_libro, Puntuacion.id_usuario == current_user.id)).first() is not None:
            raise HTTPException(status_code=400, detail="Puntuación para este usuario y libro ya existe")
        
        db_obj = Puntuacion.model_validate(
            rating, update={"id_libro": id_libro, "id_usuario": current_user.id}
        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj
    
    def get_ratings(session: Session, id_libro: int) -> list[PuntuacionPublico]:
        ratings = session.exec(select(Puntuacion).where(Puntuacion.id_libro == id_libro)).all()

        return ratings
    
    def update_rating(session: Session, current_user: Usuario, id_libro: int, rating_in: PuntuacionCrear) -> Puntuacion:   
        rating = session.exec(select(Puntuacion).where(id_libro == Puntuacion.id_libro, current_user.id == Puntuacion.id_usuario)).first()
        
        if rating is None:
            raise HTTPException(status_code=400, detail="Puntuación para este usuario y libro no existe")
        
        rating_data = rating_in.model_dump(exclude_unset=True)
        rating.sqlmodel_update(rating_data)
        session.add(rating)
        session.commit()
        session.refresh(rating)
        return rating   
    
    def delete_rating(session: Session, current_user: Usuario, id_libro: int) -> Puntuacion:
        rating = session.exec(select(Puntuacion).where(Puntuacion.id_libro == id_libro, Puntuacion.id_usuario == current_user.id)).first()
        
        if rating is None:
            raise HTTPException(status_code=400, detail="Puntuación para este usuario y libro no existe")

        session.delete(rating)
        session.commit()
        
        return rating  
    
    def get_related(session: Session, id_libro: int) -> Sequence[Libro]:
        LIMIT_BOOKS = 3
        book = session.exec(select(Libro).where(Libro.id == id_libro)).first()

        if book is None:
            raise HTTPException(status_code=404, detail="No existe libro con ese id")

        query = select(Libro)\
                .join(Libro.generos)\
                .where(or_(Libro.id_autor == book.id_autor, Genero.id.in_([genre.id for genre in book.generos])))\
                .where(Libro.id != id_libro)\
                .order_by(Libro.fecha_creacion.desc())\
                .limit(LIMIT_BOOKS)\
                .distinct()

        books = session.exec(query).all()

        if len(books) == 0:
            books = session.exec(
                select(Libro)
                .where(Libro.id != id_libro)
                .limit(LIMIT_BOOKS)
                .order_by(Libro.fecha_creacion.desc())
                .distinct()
            ).all()

        return books