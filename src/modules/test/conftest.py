from sqlalchemy import Engine
from ...database.core import get_session, seed_categories
from ...main import app
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool
from dotenv import load_dotenv
from os import getenv
import pytest


@pytest.fixture(name="engine")
def engine_fixture():
    load_dotenv()

    url = getenv("TEST_DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    engine = create_engine(
        url=url, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    return engine


@pytest.fixture(name="session")
def session_fixture(engine: Engine):
    SQLModel.metadata.create_all(engine)
    seed_categories(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app=app) as client:
        yield client
    app.dependency_overrides.clear()
