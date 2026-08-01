from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tphome.db")

engine = create_engine(DATABASE_URL)

def setup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session