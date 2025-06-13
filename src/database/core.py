from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from os import getenv
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from . import models

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
    seed_categories(None)
    yield


def seed_categories(engine_override: Engine | None):
    categories: list[models.Category] = []
    eng = engine_override or engine
    with Session(eng) as session:
        for category_name in models.CategoryName:
            exists = session.exec(
                select(models.Category).where(models.Category.name == category_name)
            ).first()
            if not exists:
                categories.append(models.Category(name=category_name))
        if categories:
            session.add_all(categories)
        session.commit()


SessionDependency = Annotated[Session, Depends(get_session)]
