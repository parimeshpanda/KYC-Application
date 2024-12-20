from . import Base,BaseMixin
from . import Column,Integer,String

class Role(Base, BaseMixin):  
    __tablename__ = "roles"  
      
    role_id = Column(Integer, primary_key=True, index=True)  
    role_name = Column(String(255)) 