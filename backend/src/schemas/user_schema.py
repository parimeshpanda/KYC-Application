from pydantic import BaseModel  
from typing import Optional  
from datetime import datetime
from pydantic import BaseModel  
from typing import List, Optional, Any, Union

class ReceivedUser(BaseModel):  
    email: Optional[str] = None  
    family_name: Optional[str] = None  
    given_name: Optional[str] = None  
    preferred_username: Optional[str] = None  



class ResponseModel(BaseModel):
    status:int
    message: Optional[str]
    data: Optional[Any]

class ErrorResponseModel(ResponseModel):
    pass

class UserDTO(BaseModel):  
    email_id: str  
    username: str  
    last_login_time: datetime
    role_id: int  
    firstname: str  
    lastname: str 
    is_admin:Optional[str] = None 
    ohr_id: str