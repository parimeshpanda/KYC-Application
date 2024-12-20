from base64 import b64decode
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.constants import Constant
from src.models.guideline_model import Guideline
from src.models.model import DocumentExtractedData, UserExtractedData
from src.models.past_records import pastRecords
from src.schemas.user_schema import ResponseModel
from sqlalchemy.exc import SQLAlchemyError

from src.services.aes_util import decrypt_data
from src.services.explaination_info import compare_info_individual, create_document_extracted_data, create_user_extracted_data

explaination_router = APIRouter(prefix=Constant.CONTEXT_PATH + "/explain") 
date_time = datetime.now()
SECRET_KEY = b64decode(Constant.SECRET_KEY) 


@explaination_router.get("/explaination-data/{thread_id}")  
async def get_data_by_thread(type: str,thread_id: str, db: Session = Depends(get_db)): 
    try:
        if type.strip().lower() =="individual":
            flag = False
            guidelines = None
            guideline_data = db.query(Guideline).first() 
            explaination_data = db.query(pastRecords.explaination).filter(pastRecords.thread_id == thread_id).first()
            user_data = db.query(UserExtractedData).filter(UserExtractedData.thread_id == thread_id).all()  
            document_data = db.query(DocumentExtractedData).filter(DocumentExtractedData.thread_id == thread_id).all() 
            kyc_stat = db.query(pastRecords).filter(pastRecords.thread_id == thread_id).first()
            kyc_stat_data = kyc_stat.kyc_status
            if kyc_stat_data =="Pass":
                flag = True
            elif kyc_stat_data == "Fail":
                flag = False
           

            if not user_data or not document_data:  
                return ResponseModel(status=404,message="Data not found in db",data ={}) 
            
            for user in user_data:
                agent_details =  {
                "Country":  user.country,  
                "First Name": decrypt_data(SECRET_KEY, user.firstname),  
                "Last Name": decrypt_data(SECRET_KEY, user.lastname),  
                "Father’s Fullname": decrypt_data(SECRET_KEY, user.father_fullname),  
                "Gender": decrypt_data(SECRET_KEY, user.gender),  
                "Date of Birth": decrypt_data(SECRET_KEY, user.date_of_birth),  
                "Marital Status": decrypt_data(SECRET_KEY, user.marital_status)
                }
            doc_coll_details = {}  
            for doc in document_data:  
                if doc.document_type == "Passport":  
                    doc_coll_details = {  
                    "First Name": decrypt_data(SECRET_KEY, doc.firstname),  
                    "Last Name": decrypt_data(SECRET_KEY, doc.lastname),  
                    "Passport No.": decrypt_data(SECRET_KEY, doc.document_number),  
                    "Passport Issue Date": decrypt_data(SECRET_KEY, doc.date_of_issue),  
                    "Passport Expiry Date": decrypt_data(SECRET_KEY, doc.date_of_expiration),  
                    "Date of Birth (DD-MM-YYYY)": decrypt_data(SECRET_KEY, doc.date_of_birth),  
                    "Place of Birth": decrypt_data(SECRET_KEY, doc.place_of_birth),  
                    "Gender": decrypt_data(SECRET_KEY, doc.gender),  
                }  
                    break  # Assuming you need only one Passport document  
                elif doc.document_type == "Social Security Card":  
                    doc_coll_details = {  
                    "SSN No.": decrypt_data(SECRET_KEY, doc.document_number),  
                    "Firstname": decrypt_data(SECRET_KEY, doc.firstname),  
                    "Lastname": decrypt_data(SECRET_KEY, doc.lastname)  
                }  
                    break  # Assuming you need only one SSN document 
            
            comparator_agent_details = []  
            if doc.document_type == "Social Security Card":
                for user, doc_info in zip(user_data, document_data):  
                    comparator_agent_details.extend([  
                    {"proofOfIdentity": "First Name", "UserProvided": decrypt_data(SECRET_KEY, user.firstname), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.firstname)},  
                    {"proofOfIdentity": "Last Name", "UserProvided": decrypt_data(SECRET_KEY, user.lastname), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.lastname)},  
                    {"proofOfIdentity": "Gender", "UserProvided": decrypt_data(SECRET_KEY, user.gender), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.gender)},  
                    {"proofOfIdentity": "Date of Birth (DD-MM-YYYY)", "UserProvided": decrypt_data(SECRET_KEY, user.date_of_birth), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.date_of_birth)},
                    {"proofOfIdentity": "SSN", "UserProvided": decrypt_data(SECRET_KEY, user.document_number), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.document_number)  }
                ])  
            elif doc.document_type == "Passport":
                for user, doc_info in zip(user_data, document_data):  
                    comparator_agent_details.extend([  
                    {"proofOfIdentity": "First Name", "UserProvided": decrypt_data(SECRET_KEY, user.firstname), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.firstname)},  
                    {"proofOfIdentity": "Last Name", "UserProvided": decrypt_data(SECRET_KEY, user.lastname), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.lastname)},  
                    {"proofOfIdentity": "Gender", "UserProvided": decrypt_data(SECRET_KEY, user.gender), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.gender)},  
                    {"proofOfIdentity": "Date of Birth (DD-MM-YYYY)", "UserProvided": decrypt_data(SECRET_KEY, user.date_of_birth), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.date_of_birth)},
                    {"proofOfIdentity": "Passport Number", "UserProvided": decrypt_data(SECRET_KEY, user.document_number), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.document_number) },
                    {"proofOfIdentity": "Issue Date (MM-DD-YYYY)", "UserProvided": decrypt_data(SECRET_KEY, user.issue_date), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.date_of_issue) },
                    {"proofOfIdentity": "Expiry Date (MM-DD-YYYY)", "UserProvided": decrypt_data(SECRET_KEY, user.expiration_date), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.date_of_expiration)},
                    {"proofOfIdentity": "Place Of Birth", "UserProvided": decrypt_data(SECRET_KEY, user.place_of_birth), "PresentUploadedDocuments": decrypt_data(SECRET_KEY, doc_info.place_of_birth)}
                ])  

            for user in user_data:
                if type.lower() =="individual" and user.country.lower() == "usa" :
                    guidelines  = guideline_data.usa_individual_guideline
                    break
                   
                elif type.lower() == "organization" and user.country.lower() == "usa":
                    guidelines  = guideline_data.usa_organization_guideline
                    break
                    
                    
            data = {  
            "explaination":explaination_data[0],
            "guidelineDetails":guidelines,
            "isKYCSuccess":flag,
            "agentDetails": agent_details,  
            "docCollDetails": doc_coll_details,  
            "comparatorAgentDetails": comparator_agent_details  
        }  
            return ResponseModel(  
                status=200,  
                message="Data retrieved successfully",  
                data=data 
            ) 
        elif type.strip().lower() == "Organization":
            return ResponseModel(status=200, message="Org data coming soon", data={})
    

    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"Error while dumping data: {str(e)}")
    except SQLAlchemyError  as ce:  
       
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(ce)}")
  
    
