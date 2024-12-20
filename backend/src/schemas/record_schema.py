

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class recordDTO(BaseModel):  
    name: str  
    thread_id: str  
    type: str  
    kycStatus: str  
    dateAdded: Optional[datetime] = None
    explaination: Optional[str] = None