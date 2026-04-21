from app.models.comunidad import ComunidadCrear, ComunidadPublica, ComunidadActualizar, UsuarioComunidad
from app.models.comunidad import ComunidadFiltro, PublicacionPublica, PublicacionCrear, Publicacion
from app.api.deps import SessionDep, CurrentUser
from app.crud.comunidad import ServicioComunidad as crud
from fastapi import APIRouter, HTTPException

from app.models.users import UsuarioPublico

router = APIRouter()

@router.post("", response_model=ComunidadPublica)
async def crear_comunidad(session: SessionDep, current_user: CurrentUser, comunidad_in: ComunidadCrear) -> ComunidadPublica:    
    comunidad_crear = ComunidadCrear.model_validate(comunidad_in, update={"id_creador": current_user.id})
    comunidad = crud.create_community(session=session, community_create=comunidad_crear)
    return comunidad


# Devuelve todas las comunidades que coincidan con el nombre
@router.get("", response_model=list[ComunidadPublica])
async def obtener_todas_comunidades(session: SessionDep, name: str | None = None) -> list[ComunidadPublica]:
    filtro = ComunidadFiltro(nombre=name)
    return crud.get_communities_by_filter(session, filtro)

@router.get("/{id_comunidad}", response_model=ComunidadPublica)
async def obtener_comunidad(session: SessionDep, id_comunidad: int) -> ComunidadPublica:
    return crud.get_community_by_id(session, id_comunidad)


@router.patch("/{id_comunidad}", response_model=ComunidadPublica)
async def actualizar_comunidad(session: SessionDep, current_user: CurrentUser, id_comunidad: int, communityEdit: ComunidadActualizar) -> ComunidadPublica:
    existing_community = crud.get_community_by_id(session, id_comunidad)

    if current_user.id != existing_community.id_creador:
        raise HTTPException(
            status_code=401,
            detail="Sólo el creador de la comunidad puede editarla",
        ) 

    return crud.edit_community(session, current_user, id_comunidad, communityEdit)

@router.post("/{id_comunidad}/members", response_model=ComunidadPublica)
async def agregar_miembro(session: SessionDep, current_user: CurrentUser, id_comunidad: int) -> ComunidadPublica:
    return crud.add_member_to_community(session, current_user, id_comunidad)

@router.get("/{id_comunidad}/members", response_model=list[UsuarioPublico])
async def obtener_miembros(session: SessionDep, id_comunidad: int) -> list[UsuarioPublico]:
    return crud.get_members(session, id_comunidad)

@router.post("/{id_comunidad}/posts", response_model=PublicacionPublica)
async def agregar_publicacion(session: SessionDep, current_user: CurrentUser, id_comunidad: int, publicacion_in: PublicacionCrear) -> PublicacionPublica:
    return crud.add_post(session, current_user, id_comunidad, publicacion_in)

@router.get("/{id_comunidad}/posts", response_model=list[PublicacionPublica])
async def obtener_publicaciones(session: SessionDep, id_comunidad: int) -> list[PublicacionPublica]:
    return crud.get_posts(session, id_comunidad)