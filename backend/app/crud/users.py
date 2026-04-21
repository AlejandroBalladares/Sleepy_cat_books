from typing import Any
from sqlalchemy import Sequence
from sqlmodel import Session, select
from app.models.users import UsuarioRegistrar, Usuario, UsuarioActualizar, Rol
from app.models.estanteria import Estanteria
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException


class ServicioUsuario(object):
    def create_user(*, session: Session, user_create: UsuarioRegistrar) -> Usuario:
        db_obj = Usuario.model_validate(
            user_create, update={"contraseña_hasheada": get_password_hash(user_create.contraseña)}
        )
        
        # Agrego las estanterias default
        db_estanteria_favoritos = Estanteria(nombre="favoritos", usuario=db_obj)
        db_estanteria_proximas_lecturas = Estanteria(nombre="proximas lecturas", usuario=db_obj)
        session.add(db_estanteria_favoritos)
        session.add(db_estanteria_proximas_lecturas)
        
        print(db_obj)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update_user(*, session: Session, current_user: Usuario, user_in: UsuarioActualizar) -> Usuario:
        if user_in.email and current_user.email != user_in.email:
            if session.exec(select(Usuario).where(Usuario.id != current_user.id, Usuario.email == user_in.email)).first() is not None:
                raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email")
        
        user_data = user_in.model_dump(exclude_unset=True)
        current_user.sqlmodel_update(user_data)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user

    def get_users(session: Session) -> Sequence[Usuario]:
        usuarios = session.exec(select(Usuario)).all()
        return usuarios
    
    def get_user_by_email(*, session: Session, email: str) -> Usuario | None:
        statement = select(Usuario).where(Usuario.email == email)
        session_user = session.exec(statement).first()
        return session_user
    
    def authenticate(*, session: Session, email: str, password: str) -> Usuario | None:
        db_user = ServicioUsuario.get_user_by_email(session=session, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.contraseña_hasheada):
            return None
        return db_user
