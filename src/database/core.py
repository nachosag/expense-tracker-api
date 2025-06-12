from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from os import getenv
from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated

load_dotenv()

url = getenv("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(url=url, echo=False, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


SessionDependency = Annotated[Session, Depends(get_session)]
