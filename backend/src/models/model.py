from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, LargeBinary, Boolean, Date, JSON, TypeDecorator, BigInteger
from . import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB



class HexByteString(TypeDecorator):
    """Convert Python bytestring to string with hexadecimal digits and back for storage."""

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None



class user_info(Base):
    __tablename__ = 'user_info'
    uuid = Column(String, primary_key=True)
    first_name = Column(String(25), nullable = True)
    last_name = Column(String(25), nullable = True)
    father_name = Column(String(50), nullable = True)
    ssn_no = Column(Integer, nullable = True)
    gender = Column(String(10), nullable = True)
    marital_status = Column(String(20), nullable = True)
    ssn_bool = Column(Boolean, nullable = True)
    aadhar_no = Column(Integer(), nullable = True)
    aadhar_bool = Column(Boolean, nullable = True)
    dl = Column(String(20), nullable = True)
    dl_bool = Column(Boolean, nullable = True)
    passport_no = Column(String(20), nullable = True)
    passport_bool = Column(Boolean, nullable = True)
    passport_link = Column(String, nullable = True)
    ssn_link = Column(String, nullable = True)
    dl_link = Column(String, nullable = True)
    aadhar_link = Column(String, nullable = True)

    aadhar_docs = relationship('doc_table_aadhar', back_populates='user')
    ssn_docs = relationship('doc_table_ssn', back_populates='user')
    dl_docs = relationship('doc_table_dl', back_populates='user')
    passport_docs = relationship('doc_table_passport', back_populates='user')
    conversation_state = relationship('conversation_state', back_populates='user')


class doc_table_aadhar(Base):
    __tablename__ = 'doc_table_aadhar'
    uuid = Column(String, ForeignKey('user_info.uuid'), primary_key=True)
    first_name = Column(String(25), nullable = True)
    last_name = Column(String(25), nullable = True)
    dob = Column(Date, nullable = True)
    aadhar_no = Column(Integer(), nullable = True)
    address = Column(String(255), nullable = True)
    aadhar_binary = Column(LargeBinary, nullable = True)

    user = relationship('user_info', back_populates='aadhar_docs')


class doc_table_ssn(Base):
    __tablename__ = 'doc_table_ssn'
    uuid = Column(String, ForeignKey('user_info.uuid'), primary_key=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    ssn_no = Column(Integer())

    user = relationship('user_info', back_populates='ssn_docs')

class doc_table_dl(Base):
    __tablename__ = 'doc_table_dl'
    uuid = Column(String, ForeignKey('user_info.uuid'), primary_key=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    dob = Column(Date)
    sex = Column(String(10))
    date_of_issue = Column(Date)
    date_of_expiry = Column(Date)
    dl_no = Column(String(30))

    user = relationship('user_info', back_populates='dl_docs')

class doc_table_passport(Base):
    __tablename__ = 'doc_table_passport'
    uuid = Column(String, ForeignKey('user_info.uuid'), primary_key=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    date_of_issue = Column(Date)
    date_of_expiry = Column(Date)
    dob = Column(Date)
    passport_no = Column(String(30))
    nationality = Column(String(25))

    user = relationship('user_info', back_populates='passport_docs')

class country_specific_info(Base):
    __tablename__ = 'country_specific_info'
    country_name = Column(String(25), primary_key=True)
    guidelines = Column(String)
    is_aadhar = Column(Boolean)
    is_passport = Column(Boolean)
    is_ssn = Column(Boolean)
    is_dl = Column(Boolean)

class conversation_state(Base):
    __tablename__ = 'conversation_state'
    uuid = Column(String, ForeignKey('user_info.uuid'), primary_key=True)
    thread_id = Column(String)
    state_obj = Column(JSON)

    user = relationship('user_info', back_populates='conversation_state')

class Checkpoints(Base):
    __tablename__ = "checkpoints"
    thread_id = Column(String, primary_key=True)
    checkpoint_ns = Column(String, primary_key = True)
    checkpoint_id = Column(String, primary_key = True)
    parent_checkpoint_id = Column(String)
    type = Column(String)
    checkpoint = Column(JSONB)
    metadata_ = Column("metadata",JSONB)
    time_stamp = Column(DateTime,default=datetime.now)  


class Userstate(Base):
    __tablename__ = 'user_state'
    # uuid = Column(String, ForeignKey('user_info.uuid'), primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(String)
    state_obj = Column(JSON)


class Jsonencrypted(Base):
    __tablename__ = 'jsonencrypted'
    id = Column(Integer, primary_key=True, autoincrement = True)
    encrypted_json = Column(HexByteString)
    private_key = Column(HexByteString)
    iv = Column(HexByteString)

class Exceldata(Base): #! NEEDS TO BE REPLACED
    __tablename__ = 'PEP_info'
    ssn_no = Column(Integer, primary_key=True)
    passport_no = Column(String)
    politically_exposed = Column(Boolean)

class TableData(Base):
    __tablename__ = 'ORG_PEP_info'
    business_license_no = Column(Integer, primary_key=True)
    high_risk_factor = Column(Boolean)

class UserExtractedData(Base):
    __tablename__ = 'user_extracted_data'
    
    id = Column(Integer, primary_key=True)
    country = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(100))
    father_fullname = Column(String(255))
    gender = Column(String(255))
    date_of_birth =  Column(String(255))   
    marital_status = Column(String(50))
    time_stamp = Column(DateTime,default=datetime.now)
    thread_id = Column(String(255)) 
    document_number = Column(String(255))
    issue_date = Column(String(255))
    expiration_date = Column(String(255))
    place_of_birth = Column(String(255))

class DocumentExtractedData(Base):
    __tablename__ = 'document_extracted_data'
    
   
    id = Column(Integer, primary_key=True)  # Primary Key with auto-increment
    document_type = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(100))
    document_number = Column(String(255))
    gender = Column(String(255))
    date_of_birth = Column(String(255)) 
    date_of_issue = Column(String(255))  
    date_of_expiration = Column(String(255)) 
    place_of_birth = Column(String(255))
    time_stamp = Column(DateTime,default=datetime.now)
    thread_id = Column(String(255)) 

class PEPData(Base):
    __tablename__ = 'PEP_data'
    
    ssn_no = Column(BigInteger, primary_key=True)
    passport_no = Column(String(10))
    politically_exposed = Column(Boolean)
    pep_user_input = Column(Boolean) 
    bank_acc_no = Column(BigInteger)
    credit_score = Column(Integer)