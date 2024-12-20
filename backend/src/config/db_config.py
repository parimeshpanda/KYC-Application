
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker  
from src.constants import Constant  
from src.models.model import Base, country_specific_info, Checkpoints, Userstate, Jsonencrypted  
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
POSTGRES_CONFIG = Constant.POSTGRES_CONFIG

  
def create_table(engine):  
    Base.metadata.create_all(engine, checkfirst=True)  # Create tables if they do not exist  
    print("Table created successfully.")  
  
def extract_usa_info(db: Session):
    try:
        
        country_info = db.query(country_specific_info).filter_by(country_name='USA_1').first()
        if country_info:
            print(country_info.guidelines)
        else:
            print("No record found for USA_1")
    except Exception as e:
        print(f"Error while fetching USA info: {e}")

def extract_agent_state(db:Session):  
    try:
     
        country_info = db.query(Userstate).order_by(Userstate.id.desc()).filter_by(thread_id=1).first()  # Ensure thread_id is an integer  
        if country_info:
                print(country_info)
        else:
                print("No record found for this thread ID")
    except Exception as e:
        print(f"Error while fetching agent state: {e}") 
  
def insert_encrypted_json(db: Session, encoded_data: str, private_key: str, iv: str):
    try:
        json_add = Jsonencrypted(
            encrypted_json=encoded_data,
            private_key=private_key,
            iv=iv
        )
        db.add(json_add)
        db.commit()
        db.refresh(json_add)
        print("Encrypted JSON inserted successfully.")
    except Exception as e:
        db.rollback()  # Rollback on error
        print(f"Error inserting encrypted JSON: {e}")

def extract_encrypted_json(db:Session,id):  
    try:
        final_json = db.query(Jsonencrypted).order_by(Jsonencrypted.id.desc()).filter_by(id=id).first()   
        if final_json:  
            return final_json  
        else:  
            print("No record found") 
    except Exception as e:
        print(f"Error fetching encrypted JSON: {e}")

def db_connection(config: dict):
    """Create and return database engine with connection pooling"""
    try:
        conn_string = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
        engine = create_engine(
            conn_string,
            poolclass=QueuePool,
            pool_size=3,  # Reduced pool size
            max_overflow=5,  # Limited overflow
            pool_timeout=30,
            pool_pre_ping=True,
            pool_recycle=1800  # 30 minutes
        )
        return engine
    except Exception as e:
        return None



@contextmanager
def get_db_session(engine) -> Session:
    """Context manager for database sessions"""
    if engine is None:
        raise ConnectionError("Database engine is not initialized")
        
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()