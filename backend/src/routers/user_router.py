import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import asc

from src.config.db import get_db
from src.constants import Constant
from src.models.Stepper import Step
from src.schemas.user_schema import ReceivedUser,ResponseModel
from sqlalchemy.orm import Session

from src.services.getUserService import insert_or_fetch_user
from src.util.azure_utils import upload_file
from src.workflows.workflow import graph

user_router = APIRouter(prefix=Constant.CONTEXT_PATH + "/user")


@user_router.post("/getUserDetails",summary="Persona Auth")
async def userDetails(ret_user:ReceivedUser,db : Session = Depends(get_db)):
    try:
        response = insert_or_fetch_user(ret_user,db)
        if response:
            ret_response = ResponseModel(**response)
            return ret_response.model_dump()
        else:
            return ResponseModel(status=200,message ="User not found",data=[])
    except ValueError as ve:  
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")  
    except ConnectionError as ce:  
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(ce)}")  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")  

@user_router.get("/steps/")  
def read_steps( db: Session = Depends(get_db)):  
    steps = db.query(Step).order_by(asc(Step.id)).all()
    ret_response = ResponseModel(status=200,message="success",data =steps)
    return ret_response.model_dump()

# @user_router.get("/steps/{thread_id}")  
# def read_steps(thread_id: str): 
#     config = {  
#         "configurable": {  
#             "user_uuid": 123123,  
#             "thread_id": thread_id,
#             "checkpoint_ns": ""
#             },
#             "recursion_limit": 100}

#     graph_state = graph.get_state(config).values
    
#     return graph_state['flags'].stepper
    


@user_router.post("/upload/{thread_id}")  
async def read_steps( thread_id:str,file: UploadFile = File(...)): 
    try: 
        file_name = get_uuid() +"-" + file.filename
        retreive = await upload_file(file, file_name)
        
        config = {  
            "configurable": {  
                "user_uuid": 123123,  
                "thread_id": thread_id,
                "checkpoint_ns": ""
                },
                "recursion_limit": 100}
        
        # State needs to be updated after the file is uploaded
        graph_state = graph.get_state(config).values
        graph_state['flags'].current_conversation_type = "conversation"

        graph.update_state(config, {"file_sas_url": retreive, "flags":graph_state['flags']})
        
        sas_response = ResponseModel(status=200,message="success",data ={"file_name":file.filename,"sas_url":retreive})
        
        return sas_response.model_dump()
    except Exception as e:
        return ResponseModel(status=500,message="File upload failed. Please try again.",data = {})

def get_uuid():
    return str(uuid.uuid4().hex)