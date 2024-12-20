from sqlalchemy import Column, Integer, String, Boolean  
from . import Base,BaseMixin

class Step(Base,BaseMixin):  
    __tablename__ = "steps"  

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)  
    icon = Column(String)  
    completed = Column(Boolean, default=False)  