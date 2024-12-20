from . import Base,BaseMixin
from . import Column,String,Integer

class Conversation(Base,BaseMixin):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    ai_question = Column(String)
    human_answer = Column(String)
    stepper = Column(String)
    timestamp = Column(String)  
    conversation_type = Column(String)
    thread_id = Column(String) 
