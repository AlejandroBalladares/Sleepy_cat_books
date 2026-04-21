from random import randint
from app.models.books import Reseña
def create_review(fake: any, max_id_usuario: int, max_id_libro: int) -> Reseña:
    return Reseña(
        contenido=fake.text(max_nb_chars=150),  # Random review content (up to 1000 characters)
        id_usuario=randint(1, max_id_usuario),  # Random user ID (within the given range)
        id_libro=randint(1, max_id_libro)  # Random book ID (within the given range)
    )