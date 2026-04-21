from faker import Faker
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app

import pytest  
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.models.users import Rol, UsuarioRegistrar

from app.main import app
from app.api.deps import get_db
from app.crud.users import ServicioUsuario
from app.initial_data import init_db

from app.tests.utils.utils import get_author_token_headers, get_reader_token_headers

@pytest.fixture(scope="session", name="session", autouse=True)
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)


    with Session(engine) as session:
        init_db(session)
        yield session

@pytest.fixture(scope="module", name="client")
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_db] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def author_token_headers(client: TestClient) -> dict[str, str]:
    return get_author_token_headers(client)

@pytest.fixture(scope="module")
def reader_token_headers(client: TestClient) -> dict[str, str]:
    return get_reader_token_headers(client)
