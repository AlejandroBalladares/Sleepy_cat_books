from random import sample
from app.models.books import LibroCrear
from app.testing.image import image_url
def create_book(faker, cantidadUsuarios: int, seed_generos: list[str]) -> LibroCrear:
    return LibroCrear(
        nombre=faker.sentence(nb_words=3),  # Random book name (title)
        isbn=faker.unique.isbn13(),  # Random unique ISBN
        fecha_publicacion=faker.date_this_century(),  # Random publication date
        descripcion=faker.text(max_nb_chars=500),  # Random description
        portada=image_url(),  # Random image URL for cover
        id_autor=faker.random_int(min=1, max=cantidadUsuarios),  # Random author ID
        generos=sample(seed_generos, k=faker.random_int(min=1, max=3))  # Random genres (1-3)
    )