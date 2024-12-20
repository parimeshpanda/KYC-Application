from . import Base,BaseMixin
from . import Column,String,Integer
from . import datetime, DateTime
   
class User(Base, BaseMixin):  
    __tablename__ = "users"  
      
    user_id = Column(Integer, primary_key=True, index=True,autoincrement=True)  
    email_id = Column(String(255), index=True)  
    username = Column(String(255),nullable=False)  
    last_login_time = Column(DateTime,default=datetime.now)  
    created_on = Column(DateTime,default=datetime.now)  
    password = Column(String(255),nullable=False)  
    role_id = Column(Integer,nullable=False)  
    firstname = Column(String(255),nullable=False)  
    lastname = Column(String(255),nullable=False)  
    ohr_id = Column(Integer,nullable=False)