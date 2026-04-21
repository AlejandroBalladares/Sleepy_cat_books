from typing import Any
from fastapi import APIRouter, HTTPException

from app.models.books import LibroCrear, LibroActualizar, LibroFiltro, LibroPublico, Genero, ReseñaCrear, ReseñaPublico, PuntuacionPublico, PuntuacionCrear
from app.models.users import Rol
from app.api.deps import SessionDep, CurrentUser
from app.crud.books import ServicioLibros as crud


router = APIRouter()

@router.post("", response_model=LibroPublico)
async def crear_libro(session: SessionDep, current_user: CurrentUser, libro_in: LibroCrear) -> LibroPublico:
    if current_user.rol is not Rol.AUTOR:
        raise HTTPException(
            status_code=401,
            detail="Sólo autores pueden crear un libro",
        ) 


    book_create = LibroCrear.model_validate(libro_in, update={"id_autor": current_user.id})
    user = crud.create_book(session=session, book_create=book_create)
    return user

@router.get("", response_model=list[LibroPublico])
async def obtener_libros(session: SessionDep, title: str | None = None, genre: str | None = None, author_name: str | None = None, author_surname: str | None = None) -> list[LibroPublico]:
    book_filter = LibroFiltro(title, genre, author_name, author_surname)
    return crud.get_books(session, book_filter)

@router.patch("/{id_libro}", response_model=LibroPublico)
async def actualizar_libro(session: SessionDep, current_user: CurrentUser, id_libro: int, bookEdit: LibroActualizar) -> LibroPublico:
    if current_user.rol is not Rol.AUTOR:
        raise HTTPException(
            status_code=401,
            detail="Sólo autores pueden editar un libro",
        ) 

    return crud.edit_book(session, current_user, id_libro, bookEdit)

@router.get("/generos", response_model=list[Genero])
async def obtener_generos(session: SessionDep) -> list[Genero]:
    return crud.get_generos(session)

@router.get("/popular", response_model=list[LibroPublico])
async def obtener_libros_populares(session: SessionDep) -> list[LibroPublico]:
    return crud.get_popular_books(session)

@router.post("/{id_libro}/reviews", response_model=ReseñaPublico)
async def crear_reseña(session: SessionDep, current_user: CurrentUser, id_libro: int, reviewCreate: ReseñaCrear) -> ReseñaPublico:
    review = crud.create_review(session, current_user, id_libro, reviewCreate)

    return ReseñaPublico(contenido=review.contenido, id_libro=review.id_libro, usuario=current_user)

@router.get("/{id_libro}/reviews", response_model=list[ReseñaPublico])
async def crear_reseña(session: SessionDep, id_libro: int) -> list[ReseñaPublico]:
    return crud.get_reviews(session, id_libro)

@router.get("/{id_libro}", response_model=LibroPublico)
async def obtener_libro(session: SessionDep, id_libro: int) -> LibroPublico:
    return crud.get_book(session, id_libro)

@router.get("/{id_libro}/related", response_model=list[LibroPublico])
async def obtener_libros_relacionados(session: SessionDep, id_libro: int) -> list[LibroPublico]:
    return crud.get_related(session, id_libro)

@router.post("/{id_libro}/ratings", response_model=PuntuacionPublico)
async def crear_puntuacion(session: SessionDep, current_user: CurrentUser, id_libro: int, ratingCreate: PuntuacionCrear) -> PuntuacionPublico:
    rating = crud.create_rating(session, current_user, id_libro, ratingCreate)

    return rating

@router.get("/{id_libro}/ratings", response_model=list[PuntuacionPublico])
async def obtener_puntuaciones(session: SessionDep, id_libro: int) -> list[PuntuacionPublico]:
    return crud.get_ratings(session, id_libro)

@router.patch("/{id_libro}/ratings", response_model=PuntuacionPublico)
async def actualizar_puntuacion(session: SessionDep, current_user: CurrentUser, id_libro: int, ratingCreate: PuntuacionCrear) -> PuntuacionPublico:
    rating = crud.update_rating(session, current_user, id_libro, ratingCreate)

    return rating

@router.delete("/{id_libro}/ratings", response_model=PuntuacionPublico)
async def eliminar_puntuacion(session: SessionDep, current_user: CurrentUser, id_libro: int) -> PuntuacionPublico:
    rating = crud.delete_rating(session, current_user, id_libro)

    return rating
