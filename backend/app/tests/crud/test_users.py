from faker import Faker
from sqlmodel import Session
from app.models.users import UsuarioRegistrar
from app.crud.users import ServicioUsuario as crud


def test_create_user(session: Session) -> None:
    fake = Faker()
    
    name = fake.name()
    email = fake.email()

    usuario = UsuarioRegistrar(
      nombre=name,
      contraseña= "password",
      email= email,
      apellido= "Robinson",
      nombre_de_usuario= fake.user_name(),
      fecha_nacimiento= "1979-04-20",
      rol= "LECTOR"
    )

    crud.create_user(session=session, user_create=usuario)
    result = crud.get_user_by_email(session=session, email=email)

    assert result is not None
    assert result.nombre == name
    assert result.estanterias is not None
    assert len(result.estanterias) == 2
    assert result.estanterias[0].nombre == "favoritos"
    assert result.estanterias[1].nombre == "proximas lecturas"