# database setup file
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Simple SQLite database in a project file.
DATABASE_URL = "sqlite:///./manga_store.db"

# create the sqlite connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory for working with the database.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# base class for tables
Base = declarative_base()


def get_session() -> Session:
    # Return a new session for queries.
    return SessionLocal()
