from pydantic import BaseModel  

class StepBase(BaseModel):  
    name: str  
    icon: str  
    completed: bool  

class StepCreate(StepBase):  
    pass  

class Step(StepBase):  
    id: int  

    class Config:  
        getattr = True  