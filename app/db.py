# файл с настройкой базы
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Простая база SQLite в файле проекта.
DATABASE_URL = "sqlite:///./manga_store.db"

# создаем подключение к sqlite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Фабрика сессий для работы с базой.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# базовый класс для таблиц
Base = declarative_base()


def get_session() -> Session:
    # Возвращаем новую сессию для запросов.
    return SessionLocal()
