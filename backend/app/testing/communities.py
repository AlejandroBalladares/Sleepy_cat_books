from random import randint, random
from app.models.comunidad import ComunidadCrear, TipoComunidad
from app.testing.image import image_url
def create_community(fake: any, max_id_creador: int = 1000) -> ComunidadCrear:
    return ComunidadCrear(
        nombre=fake.company(),  # Random community name (company name is a good proxy)
        imagen=image_url() if fake.boolean(85) else None,  # Random image URL or None
        tipo=TipoComunidad.PUBLICO,  # Por ahora son todas públicas
        id_creador=randint(1, max_id_creador),  # Random creator ID or None
        descripcion=fake.text(max_nb_chars=300) if fake.boolean(chance_of_getting_true=85) else None  # Random description or None
    )