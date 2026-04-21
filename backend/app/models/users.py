from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from enum import Enum
from datetime import datetime, date
from typing import Optional

class Rol(str, Enum):
    LECTOR = "LECTOR"
    AUTOR = "AUTOR"
    ADMIN = "ADMIN"

class UsuarioBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    nombre: str = Field(max_length=255)
    apellido: str = Field(max_length=255)
    nombre_de_usuario: str = Field(unique=True)
    fecha_nacimiento: date
    rol: Rol
    descripcion: str | None = None
    foto_de_perfil: str | None = None # Probe con tipo url y SQLAlchemy no lo reconoce
    
class UsuarioLogin(SQLModel):
    email: EmailStr
    contraseña: str

class UsuarioRegistrar(SQLModel):
    contraseña: str = Field(min_length=8, max_length=40)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    nombre: str = Field(min_length=1, max_length=255)
    apellido: str = Field(min_length=1, max_length=255)
    nombre_de_usuario: str = Field(min_length=1, unique=True)
    fecha_nacimiento: date
    rol: Rol


# Database model, database table inferred from class name
class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    contraseña_hasheada: str
    fecha_creacion: datetime = Field(
        default_factory=datetime.now
    )
    
    estanterias: list["Estanteria"] = Relationship(back_populates="usuario")
    publicaciones: list["Publicacion"] = Relationship(back_populates="usuario")
    # comunidades: list["Comunidad"] = Relationship(back_populates="usuarios", link_model="UsuarioComunidad")
    # comunidades: list["Comunidad"] = Relationship(back_populates="usuarios", link_model="UsuarioComunidad")


class UsuarioPublico(UsuarioBase):
    id: int
    
class UsuarioActualizar(SQLModel):
    email: Optional[EmailStr] = Field(None, unique=True, index=True, max_length=255)
    nombre: Optional[str] = Field(None, max_length=255)
    apellido: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = Field(default=None)
    foto_de_perfil: Optional[str] = Field(default=None)