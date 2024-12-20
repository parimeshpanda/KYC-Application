from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel 

class Message(BaseModel):  
    id: str  
    ai_question: Optional[str]=None   
    human_answer: Optional[str] = None
    stepper: Optional[str] = None
    timestamp: Optional[str] = None
    conversation_type: Optional[str] = None
    comparator_state: Optional[dict] = None
  
class ConversationPayload(BaseModel):  
    thread_id: str  
    result: Optional[Message] =None
    