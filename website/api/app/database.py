import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database set up
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@db:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
