from typing import Annotated
from sqlmodel import create_engine, SQLModel, Session
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

url = getenv("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(url=url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
    session.close()


def create_db_and_tables():
    from . import models  # type: ignore  # noqa: F401

    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


SessionDependency = Annotated[Session, Depends(get_session)]
