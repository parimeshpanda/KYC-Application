from . import Base,BaseMixin
from . import Column,Integer,String
  

  
class Guideline(Base,BaseMixin):  
    __tablename__ = "guidelines"  
  
    id = Column(Integer, primary_key=True, index=True)  
    usa_individual_guideline = Column(String(255), nullable=False)  
    usa_organization_guideline = Column(String(255), nullable=False)  
  
