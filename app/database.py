import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

logger = logging.getLogger("uvicorn")

Base = declarative_base()

def create_db_engine():
    db_url = settings.DATABASE_URL
    try:
        if db_url.startswith("sqlite"):
            engine = create_engine(
                db_url,
                connect_args={"check_same_thread": False}
            )
        else:
            # PostgreSQL engine
            engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20
            )
            # Test immediate connection
            with engine.connect() as conn:
                logger.info("Successfully connected to PostgreSQL database.")
        return engine
    except Exception as e:
        if settings.FALLBACK_TO_SQLITE:
            logger.warning(
                f"Could not connect to PostgreSQL at {db_url}: {e}.\n"
                "Falling back to local SQLite database (college_events.db) so you can develop immediately."
            )
            sqlite_engine = create_engine(
                "sqlite:///./college_events.db",
                connect_args={"check_same_thread": False}
            )
            return sqlite_engine
        else:
            raise e

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
