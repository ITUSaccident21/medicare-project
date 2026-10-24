from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Kết nối CSDL PostgreSQL Supabase hoặc SQLite test
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency cung cấp session kết nối CSDL cho FastAPI endpoint."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
