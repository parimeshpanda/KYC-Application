from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

from src.constants import Constant  
# from src.config.db_config import POSTGRES_CONFIG 
POSTGRES_CONFIG = Constant.POSTGRES_CONFIG 
  
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['dbname']}"  
  
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=100, max_overflow=20,pool_pre_ping=True)  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()  
  
def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close()  
class BaseMixin:
    def model_dump(self):  
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}