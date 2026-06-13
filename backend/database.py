import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # tests connection before using it
    pool_recycle=300,          # recycle connections every 5 minutes
    pool_size=5,               # max 5 connections in pool
    max_overflow=10            # allow 10 extra connections if needed
)

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    autocommit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()