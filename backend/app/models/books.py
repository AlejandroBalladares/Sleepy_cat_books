from dataclasses import dataclass
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, date, timezone
from app.models.estanteria import LibroEstanteria, Estanteria
from app.models.users import Usuario, UsuarioPublico  

class LibroGenero(SQLModel, table=True):
    id_libro: int = Field(foreign_key="libro.id", primary_key=True)
    id_genero: int = Field(foreign_key="genero.id", primary_key=True)

class LibroImagenIlustrativa(SQLModel, table=True):
    id_imagenes_ilustrativas: int = Field(default=None, foreign_key="imagenilustrativa.id", primary_key=True)
    id_libro: int = Field(default=None, foreign_key="libro.id", primary_key=True)

class LibroBase(SQLModel):
    nombre: str = Field(min_length=1, index=True)
    isbn: str = Field(min_length=1, index=True, unique=True)
    fecha_publicacion: date 
    descripcion: str = Field(min_length=1)
    portada: str | None
    id_autor: None | int = Field(foreign_key="usuario.id")

class Libro(LibroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    generos: list["Genero"] = Relationship(back_populates="libros", link_model=LibroGenero)
    
    estanterias: list["Estanteria"] = Relationship(back_populates="libros", link_model=LibroEstanteria)
    
    imagenes_ilustrativas: list["ImagenIlustrativa"] = Relationship(back_populates="libro", link_model=LibroImagenIlustrativa)

class Genero(SQLModel, table=True):
    id: int = Field(index=True, primary_key=True)
    nombre: str = Field(unique=True)
    libros: list["Libro"] | None = Relationship(back_populates="generos", link_model=LibroGenero)

class ImagenIlustrativa(SQLModel, table=True):
    id: int | None = Field(index=True, primary_key=True)
    url: str | None = Field(default=None)
    libro: "Libro" = Relationship(back_populates="imagenes_ilustrativas", link_model=LibroImagenIlustrativa)

class LibroCrear(SQLModel):
    nombre: str = Field(min_length=1)
    isbn: str = Field(min_length=1, index=True, unique=True)
    fecha_publicacion: date
    descripcion: str = Field(min_length=1)
    portada: str | None = Field(default=None)
    id_autor: int | None = Field(default=None)
    generos: list[str]

class LibroPublico(LibroBase):
    id: int
    generos: list[Genero]
    imagenes_ilustrativas: list[ImagenIlustrativa]

class LibroActualizar(SQLModel):
    nombre: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = Field(None, min_length=1)
    portada: Optional[str] = Field(default=None)
    imagenes_ilustrativas: list[str | None] = Field(default=None, max_items=3)

@dataclass
class LibroFiltro():
    title: str | None = None
    genre: str | None = None
    author_name: str | None = None
    author_surname: str | None = None

class ReseñaBase(SQLModel):
    contenido: str = Field(min_length=1, max_length=1000)

class ReseñaCrear(ReseñaBase):
    pass

class ReseñaPublico(ReseñaBase):
    id_libro: int
    usuario: UsuarioPublico = None

class Reseña(ReseñaBase, table=True):
    id_usuario: int = Field(foreign_key="usuario.id", primary_key=True)
    id_libro: int = Field(foreign_key="libro.id", primary_key=True)
    
class PuntuacionBase(SQLModel):
    puntuacion: int = Field(ge=1, le=5)

class PuntuacionCrear(PuntuacionBase):
    pass

class PuntuacionPublico(PuntuacionBase):
    id_libro: int
    id_usuario: int

class Puntuacion(PuntuacionBase, table=True):
    id_usuario: int = Field(foreign_key="usuario.id", primary_key=True)
    id_libro: int = Field(foreign_key="libro.id", primary_key=True)