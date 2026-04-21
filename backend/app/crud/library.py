from sqlmodel import Session, select
from app.models.books import Libro, LibroPublico
from app.models.users import Usuario
from app.models.estanteria import Estanteria
from fastapi import HTTPException

class ServicioBiblioteca(object):
    def add_book(*, session: Session, current_user: Usuario, nombre_estanteria: str, id_libro: int ) -> Estanteria:
        estanteria = next((estanteria for estanteria in current_user.estanterias if estanteria.nombre == nombre_estanteria), None)
        if estanteria is None:
          raise HTTPException(status_code=404, detail="No existe esa estantería")
        
        db_libro = session.exec(select(Libro).where(Libro.id==id_libro)).first()
        if db_libro is None:
          raise HTTPException(status_code=404, detail="No existe un libro con ese id")
        
        estanteria.libros.append(db_libro)     
        
        print(estanteria)
        try:
          session.add(estanteria)
          session.commit()
          session.refresh(estanteria)
        except Exception as _e:
          session.rollback()
          raise HTTPException(status_code=409, detail="Este libro ya está en la estantería")
        
        return estanteria
      
    def get_books_from_shelf(*, session: Session, current_user: Usuario, nombre_estanteria: str) -> list[LibroPublico]:
      estanteria = next((estanteria for estanteria in current_user.estanterias if estanteria.nombre == nombre_estanteria), None)
      if estanteria is None:
          raise HTTPException(status_code=404, detail="No existe esa estantería")
        
      return estanteria.libros
    
    def delete_book_from_shelf(*, session: Session, current_user: Usuario, nombre_estanteria: str, id_libro: int) -> LibroPublico:
      estanteria = next((estanteria for estanteria in current_user.estanterias if estanteria.nombre == nombre_estanteria), None)
      if estanteria is None:
        raise HTTPException(status_code=404, detail="No existe esa estantería")
      
      libro = session.exec(select(Libro).where(Libro.id == id_libro)).first()

      if libro is None:
        raise HTTPException(status_code=404, detail="No existe un libro con ese id")

      for libro_estanteria in estanteria.libros:
        if libro_estanteria.id == libro.id:
          estanteria.libros.remove(libro)
          session.add(libro)
          session.commit()
          return libro

      raise HTTPException(status_code=404, detail="Este libro no está en la estantería")
    
    def get_shelves(*, session: Session, current_user: Usuario) -> list[Estanteria]:
        return current_user.estanterias  
      