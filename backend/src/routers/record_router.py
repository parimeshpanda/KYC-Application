
from base64 import b64decode
from datetime import datetime
import json
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, desc, func
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.constants import Constant
from src.models.Conversations import Conversation
from src.models.model import Checkpoints
from src.schemas.record_schema import  recordDTO
from src.models.past_records import pastRecords
from src.schemas.user_schema import ResponseModel
from src.constants import Constant
from src.services.aes_util import decrypt_data, encrypt_data
from sqlalchemy.exc import SQLAlchemyError
import pytz 
from src.services.explaination_info import compare_info_individual
# In a real application, you should securely store ###  
SECRET_KEY = b64decode(Constant.SECRET_KEY)

record_router = APIRouter(prefix=Constant.CONTEXT_PATH + "/records") 
@record_router.post("/pastRecordsInsert")  
def create_user(user: recordDTO, db: Session = Depends(get_db)):  
    try:
        existing_record = db.query(pastRecords).filter_by(thread_id=user.thread_id).first()  
        if existing_record:  
            return ResponseModel(status=200, message=f"Thread ID {user.thread_id} already exists", data={})  
        time_zone = pytz.timezone('Asia/Calcutta')  
        utc_time  =datetime.now(pytz.utc)
        india_time = utc_time.astimezone(time_zone)
        db_user = pastRecords(  
            name=user.name,  
            thread_id=user.thread_id,  
            type=user.type,  
            kyc_status=user.kycStatus,  
            date_added= india_time ,
            explaination = user.explaination
        )  
        # latest_checkpoint = db.query(Checkpoints) \
        #     .filter(Checkpoints.thread_id == user.thread_id) \
        #     .order_by(Checkpoints.time_stamp.desc()) \
        #     .first() 
        # if latest_checkpoint:
        #     stmt_checkpoints = delete(Checkpoints) \
        #         .where(Checkpoints.thread_id == user.thread_id) \
        #         .where(Checkpoints.time_stamp != latest_checkpoint.time_stamp)  # Keep the most recent record
        #     db.execute(stmt_checkpoints)
        #     db.commit()

        # stmt_checkpoints = delete(Checkpoints).where(Checkpoints.thread_id == user.thread_id)  
        # db.execute(stmt_checkpoints)  
        # db.commit()
        if user.type == "Individual":
            compare_info_individual(user.thread_id, db) # individual explaination added
        elif user.type == "Organization":
            pass
        redis_data = fetch_data_from_redis(db_user.thread_id)
        if not redis_data:
            raise HTTPException(status_code=404, detail="No data found in Redis")
        thread_id = db_user.thread_id
        conversations = [] 
        for index, item in enumerate(redis_data):
            if index == 0:
                continue  

            conversation = Conversation(
                ai_question=encrypt_data(SECRET_KEY,item["ai_question"]),
                human_answer=encrypt_data(SECRET_KEY,item["human_answer"]),
                stepper=item["stepper"],
                timestamp=item["timestamp"],
                conversation_type=item["conversation_type"],
                thread_id=thread_id  
            )
            conversations.append(conversation) 
        db.add(db_user)
        db.bulk_save_objects(conversations)
        db.commit()
        db.refresh(db_user)

        
        return  ResponseModel(status=200,message="Success",data =f"Successfully added to db with threadID {thread_id} ")
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error while dumping data: {str(e)}")
    except SQLAlchemyError  as ce:  
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(ce)}")
  
@record_router.get("/pastRecordList")  
def read_user( db: Session = Depends(get_db)):  
    data =db.query(pastRecords).order_by(desc(pastRecords.date_added)).all()
    data_dict = [
            {key: value for key, value in vars(record).items() if not key.startswith('_') and key != 'explanation'}
            for record in data
        ]
    return ResponseModel(status=200,message="Success",data =data_dict)

@record_router.get("/pastRecordById/{thread_id}")  
def get_record_by_id(thread_id:str,db:Session = Depends(get_db)):
    data = db.query(Conversation).filter(Conversation.thread_id == thread_id).all()
    data_dict = [  
        {  
            key: decrypt_data(SECRET_KEY, value) if key in ["ai_question", "human_answer"] else value  
            for key, value in vars(record).items() if not key.startswith('_')  
        }  
        for record in data  
    ]  
    return ResponseModel(status=200,message="Success",data =data_dict)


def fetch_data_from_redis(redis_key:str) -> List[Dict]:

    client = Constant.REDIS_CONN
    data = client.get(redis_key)
    if data:
        return json.loads(data)
    return []

# @record_router.post("/dump_redis_to_db")
# def dump_redis_to_db(redis_key: str, db: Session = Depends(get_db)):
#     try:
#         redis_data = fetch_data_from_redis(redis_key=redis_key)
#         if not redis_data:
#             raise HTTPException(status_code=404, detail="No data found in Redis")

#         thread_id = redis_key
#         for index, item in enumerate(redis_data):
#             if index == 0:
#                 continue  # Skip the first iteration

#             conversation = Conversation(
#                 ai_question=item["ai_question"],
#                 human_answer=item["human_answer"],
#                 stepper=item["stepper"],
#                 timestamp=item["timestamp"],
#                 conversation_type=item["conversation_type"],
#                 thread_id=thread_id  # Use the Redis key as thread_id
#             )
#             db.add(conversation)

#         # Commit the transaction to PostgreSQL
#         db.commit()
#         return {"message": "Data successfully dumped into PostgreSQL"}

#     except Exception as e:
#         db.rollback()  # Rollback in case of error
#         raise HTTPException(status_code=500, detail=f"Error while dumping data: {str(e)}")