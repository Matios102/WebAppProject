from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from app.core.config import settings

DATABASE = settings.DATABASE_URL

engine = None
SessionLocal = None 
Base = declarative_base()

try:
    engine = create_engine(DATABASE)
    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    print("Database connection successful.")

except OperationalError as e:
    print("Could not connect to the database. Exception: ", e)
    engine = None
    SessionLocal = None

def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database connection is not available.") 
     
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()