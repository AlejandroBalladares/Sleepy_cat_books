from dataclasses import dataclass
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from app.models.users import Usuario, UsuarioPublico
from typing import List, Optional
from datetime import datetime, timezone

# Para relascion muchos a muchos
class UsuarioComunidad(SQLModel, table=True):
    id_usuario: int = Field(foreign_key="usuario.id", primary_key=True)
    id_comunidad: int = Field(foreign_key="comunidad.id", primary_key=True)

class TipoComunidad(str, Enum):
    PUBLICO = "Publico"
    PRIVADO = "Privado"

class ComunidadBase(SQLModel):
    nombre: str = Field(min_length=1, index=True)
    imagen: str | None
    tipo: TipoComunidad
    id_creador: None | int = Field(foreign_key="usuario.id") #Relationship(link_model="Usuario", sa_relationship_kwargs={"primaryjoin": "Comunidad.id_creador==Usuario.id"}) 
    descripcion: str | None = None

class Comunidad(ComunidadBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # usuarios: list["Usuario"] = Relationship(back_populates="comunidades", link_model="UsuarioComunidad")

class ComunidadCrear(SQLModel):
    nombre: str = Field(min_length=1)
    imagen: None | str = None             # agregarle una imagen default a la comunidad?
    tipo: TipoComunidad = TipoComunidad.PUBLICO
    id_creador: None | int = Field(default=None)
    descripcion: None | str = None

class ComunidadPublica(ComunidadBase):
    id: int
    # usuarios: list["UsuarioPublico"]

class ComunidadActualizar(SQLModel):
    nombre: Optional[str] = Field(None, min_length=1)
    tipo: Optional[TipoComunidad] = None
    imagen: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(None, min_length=1)


@dataclass
class ComunidadFiltro():
    nombre: str | None = None
     
class PublicacionBase(SQLModel):
    contenido: str

class PublicacionCrear(PublicacionBase):
    imagenes: list[str | None] = Field(default=None)

class PublicacionPublica(SQLModel):
    id: int
    id_usuario: int
    id_comunidad: int
    contenido: str
    
    fecha: datetime 
    
    usuario: UsuarioPublico
    
    imagenes: list['ImagenPublicacion']

class ImagenPublicacionLink(SQLModel, table=True):
    id_imagenes: int = Field(default=None, foreign_key="imagenpublicacion.id", primary_key=True)
    id_publicacion: int = Field(default=None, foreign_key="publicacion.id", primary_key=True)
    
class Publicacion(PublicacionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id")
    id_comunidad: int = Field(foreign_key="comunidad.id")
    
    fecha: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )    
    
    usuario: Usuario = Relationship(back_populates="publicaciones")
    
    imagenes: list["ImagenPublicacion"] = Relationship(back_populates="publicacion", link_model=ImagenPublicacionLink)

class ImagenPublicacion(SQLModel, table=True):
    id: int | None = Field(index=True, primary_key=True)
    url: str | None = Field(default=None)
    publicacion: Publicacion = Relationship(back_populates="imagenes", link_model=ImagenPublicacionLink)