from fastapi import APIRouter

from app.models.estanteria import Estanteria, AgregarLibro, EstanteriaPublica
from app.models.books import LibroPublico
from app.api.deps import SessionDep, CurrentUser
from app.crud.library import ServicioBiblioteca as crud


router = APIRouter()

@router.post("/{nombre_estanteria}", response_model=Estanteria)
async def agregar_libro(session: SessionDep, current_user: CurrentUser, nombre_estanteria: str, agregar_libro: AgregarLibro) -> Estanteria: 
    id_libro = agregar_libro.id_libro
    
    return crud.add_book(session=session, current_user=current_user, nombre_estanteria=nombre_estanteria, id_libro=id_libro)

@router.get("/{nombre_estanteria}", response_model=list[LibroPublico])
async def obtener_libros_de_estanteria(session: SessionDep, current_user: CurrentUser, nombre_estanteria: str) -> list[LibroPublico]:
    return crud.get_books_from_shelf(session=session, current_user=current_user, nombre_estanteria=nombre_estanteria)    

@router.delete("/{nombre_estanteria}/{id_libro}", response_model=LibroPublico)
async def eliminar_libro_de_estanteria(session: SessionDep, current_user: CurrentUser, nombre_estanteria: str, id_libro: int) -> LibroPublico:
    return crud.delete_book_from_shelf(session=session, current_user=current_user, nombre_estanteria=nombre_estanteria, id_libro=id_libro)

@router.get("", response_model=list[EstanteriaPublica])
async def obtener_estanterias(session: SessionDep, current_user: CurrentUser) -> list[EstanteriaPublica]: 
    return crud.get_shelves(session=session, current_user=current_user)