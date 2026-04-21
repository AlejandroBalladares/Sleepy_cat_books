from sqlmodel import Field, Relationship, SQLModel
from app.models.users import Usuario
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.books import Libro

class LibroEstanteria(SQLModel, table=True):
    id_libro: int = Field(foreign_key="libro.id", primary_key=True)
    id_estanteria: int = Field(foreign_key="estanteria.id", primary_key=True)

class Estanteria(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Usuario = Relationship(back_populates="estanterias")
    
    libros: list["Libro"] = Relationship(back_populates="estanterias", link_model=LibroEstanteria)
    
class AgregarLibro(SQLModel):
    id_libro: int
    
class EstanteriaPublica(SQLModel): 
    nombre: str