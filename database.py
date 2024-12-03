from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore

SQLALCHEMY_DATABASE_URL = 'sqlite:///./app.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
   db = sessionLocal()
   try:
      yield db
   finally:
      db.close()
