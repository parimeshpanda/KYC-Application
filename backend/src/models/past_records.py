from datetime import datetime
from sqlalchemy import DateTime
from . import Base,BaseMixin
from . import Column,Integer,String

class pastRecords(Base,BaseMixin):  
    __tablename__ = 'past_records'  
      
    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String(255))  
    thread_id = Column(String(255)) 
    type = Column(String(50))  
    kyc_status = Column(String(50))  
    date_added =Column(DateTime,default=datetime.now)  
    explaination = Column(String(3000)) 