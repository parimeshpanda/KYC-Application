import os
import json 
from src.models.agent_state import AgentState
from sqlalchemy.ext.declarative import declarative_base
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TypeDecorator
from langchain_core.messages import SystemMessage
from src.constants import Constant
class HexByteString(TypeDecorator):
    """Convert Python bytestring to string with hexadecimal digits and back for storage."""

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None
    
Base = declarative_base()
class Jsonencrypted(Base):
    __tablename__ = 'jsonencrypted'
    id = Column(Integer, primary_key=True, autoincrement = True)
    encrypted_json = Column(HexByteString)
    private_key = Column(HexByteString)
    iv = Column(HexByteString)
 

POSTGRES_CONFIG = Constant.POSTGRES_CONFIG

def db_connection(config):
    try:
        conn_string = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
        engine = create_engine(conn_string)
        print("Connected to the database successfully.")
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    
def store_agent_state(encoded_data, private_key, iv):
    engine = db_connection(POSTGRES_CONFIG)
    Session = sessionmaker(bind=engine)
    session = Session()
    json_add = Jsonencrypted(
        encrypted_json = encoded_data,
        private_key = private_key,
        iv = iv
    )
    session.add(json_add)
    session.commit()
    session.close()

def generate_key_iv():
    key = os.urandom(32)
    iv = os.urandom(16)
    return key, iv

def aes_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data
    
def encryption(Userstate:str):
    # x = {"all_info":state["user_information"].json()}
    # x= Userstate
    # json_data = json.load(Userstate)
    key, iv = generate_key_iv()
    encrypted_data = aes_encrypt(Userstate, key, iv)
    store_agent_state(encrypted_data, key, iv)


    with open('encrypted_data.bin', 'wb') as enc_file:
        enc_file.write(encrypted_data)

def save_info(state: AgentState) -> None:
    """
    Save and encrypt user information from agent state
    
    Args:
        state: LangGraph AgentState object containing user information
    """
    try:
        if state.initial_state.kyc_for=="Individual":
            Userstate = repr(state.user_information)
        elif state.initial_state.kyc_for=="Organization":
            Userstate= repr(state.all_board_member_information)
        else:
            raise KeyError("user_information not found in state")
        # Call encryption function with the JSON string
        encryption(Userstate)
        return {"history":[SystemMessage(content="User has provided the required information. The information has been saved to the database.")]}

    except AttributeError as e:
        print(f"Error accessing state attributes: {e}")
    except json.JSONDecodeError as e:
        print(f"Error encoding state to JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")