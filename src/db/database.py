from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from config import (
    SUPABASE_DBNAME,
    SUPABASE_HOST,
    SUPABASE_PASSWORD,
    SUPABASE_PORT,
    SUPABASE_USER,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URL = f"postgresql+psycopg2://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:{SUPABASE_PORT}/{SUPABASE_DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Session:  # type: ignore
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_session() -> Session:
    """Get a database session (for non-context manager usage)"""
    return SessionLocal()
