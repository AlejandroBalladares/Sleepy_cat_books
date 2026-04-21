from random import choice
from app.models.users import Rol, UsuarioRegistrar
def create_user(fake) -> UsuarioRegistrar:
    return UsuarioRegistrar(
        contraseña=fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),  # Random password
        email=fake.unique.email(),  # Random email address
        nombre=fake.first_name(),  # Random first name
        apellido=fake.last_name(),  # Random last name
        nombre_de_usuario=fake.user_name(),  # Random username
        fecha_nacimiento=fake.date_of_birth(minimum_age=18),  # Random birthdate
        rol=choice([Rol.LECTOR, Rol.AUTOR, Rol.ADMIN])  # Random role from the Rol enum
    )