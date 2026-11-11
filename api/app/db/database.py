from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import inspect, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tphome.db")

engine = create_engine(DATABASE_URL)

# Columns added after the table was first created, create_all() doesn't add them
_ADDED_COLUMNS = {
    "blind": {"locked": "BOOLEAN NOT NULL DEFAULT 0"},
}


def setup():
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    with engine.begin() as conn:
        for table, columns in _ADDED_COLUMNS.items():
            existing = {c["name"] for c in inspector.get_columns(table)}
            for name, ddl in columns.items():
                if name not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))

def get_session():
    with Session(engine) as session:
        yield session