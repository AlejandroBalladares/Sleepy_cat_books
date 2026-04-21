from fastapi import APIRouter, HTTPException

from app.models.users import UsuarioPublico, UsuarioRegistrar, UsuarioActualizar, Rol
from app.api.deps import SessionDep,CurrentUser
from app.crud.users import ServicioUsuario as crud


router = APIRouter()

@router.post("/signup", response_model=UsuarioPublico)
async def registrar_usuario(session: SessionDep, user_in: UsuarioRegistrar) -> UsuarioPublico:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con este email",
        )
    user_create = UsuarioRegistrar.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_create)
    return user

@router.get("/me", response_model=UsuarioPublico)
async def obtener_usuario(session: SessionDep, current_user: CurrentUser) -> UsuarioPublico:
    return current_user

@router.patch("/me", response_model=UsuarioPublico)
async def actualizar(session: SessionDep, current_user: CurrentUser, user_in: UsuarioActualizar) -> UsuarioPublico:
    return crud.update_user(session=session, current_user=current_user, user_in=user_in)

@router.get("/", response_model=list[UsuarioPublico])
async def obtener_usuarios(session: SessionDep) -> list[UsuarioPublico]:
    return crud.get_users(session)
