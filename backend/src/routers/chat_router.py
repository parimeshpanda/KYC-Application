import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
import random
import uuid
from fastapi import APIRouter, Depends, HTTPException  
from pydantic import BaseModel  
from typing import Dict, Any
from loguru import logger
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.constants import Constant
from src.schemas.message_convo_schema import ConversationPayload, Message
from src.schemas.user_schema import ResponseModel
from src.services.redis_service import append_to_redis, initialize_conversation, read_conversation_from_redis
from src.workflows.workflow import re_run_graph, run_graph, graph
from src.constants import Constant
import time
import re

r = Constant.REDIS_CONN
chatrouter = APIRouter(prefix=Constant.CONTEXT_PATH + "/chat")  
executor = ThreadPoolExecutor(max_workers=5) 
async def run_in_executor(func, *args):  
    loop = asyncio.get_event_loop()  
    return await loop.run_in_executor(executor, func, *args) 

def transform(s):  
    # Check if the string contains any digits  
    if re.search(r'\d', s):  
        return s.upper()  
    else:  
        return s.lower() 

@chatrouter.post("/startChat")  
def start_conversation():  
    thread_id = str(random.randint(100000, 999999))   
    initialize_conversation(thread_id)  
    
    return {"thread_id": thread_id}  
   

@chatrouter.post("/startConversation")  
async def send_message(payload: ConversationPayload):  

    try:  
        config = {  
            "configurable": {  
                "user_uuid": 123123,  
                "thread_id": payload.thread_id,  
                "checkpoint_ns": ""  
            },  
            "recursion_limit": 100,  
        }  
        def get_state_and_run_graph():
            gs = graph.get_state(config)
            
            if gs.values == {}:
                result = run_graph(config)
                logger.info("INITIAL RESULT: ", repr(result))
                return result
            
            else:
                last_user_message = payload.result.human_answer if payload.result else ""  
                transform_message = transform(last_user_message)
                print(transform_message)  
                result = re_run_graph(transform_message, config)  
                logger.info(f"re-run results: {repr(result)}")
                return result
        result = await run_in_executor(get_state_and_run_graph) 
        response_message = Message(  
            id=str(uuid.uuid4()),  
            ai_question=result['response'],  
            human_answer="",  
            timestamp=datetime.now().isoformat() ,
            stepper=result['stepper'],
            conversation_type=result['conversation_type'],
            comparator_state = result['comparator_state']
        )  

        # Append the messages received from the UI to Redis  
        data_to_store = payload.result.model_dump()
        if 'comparator_state' in data_to_store:
            del data_to_store['comparator_state'] 
        if payload.result:  
            append_to_redis(payload.thread_id, {  
                "thread_id": payload.thread_id,  
                "result": data_to_store 
            })  

        res = response_message.model_dump()  
        logger.info(f"data response:{res}")  

        return {"status": 200, "message": "Success", "data": {"thread_id": payload.thread_id, "result": res}}  

    except Exception as e:  
        logger.error(f"An exception occurred: {e}")  
        raise HTTPException(status_code=500, detail=str(e))  
  
@chatrouter.get("/getChatHistory/{thread_id}")  
def get_chat_history(thread_id: str):  
    try:  
        conversation = read_conversation_from_redis(thread_id)  
        if conversation[1:]:
            return { "result": conversation[1:]}  
    except Exception as e:  
        logger.error(f"An exception occurred: {e}")  
        raise HTTPException(status_code=500, detail=str(e))  