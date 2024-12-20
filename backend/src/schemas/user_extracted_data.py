from typing import Dict, List, Optional
from pydantic import BaseModel  
from datetime import date  
  
class UserCreate(BaseModel):  
    country:  Optional[str] =None  
    firstname: Optional[str] =None 
    lastname:  Optional[str] =None  
    father_fullname:  Optional[str] =None  
    gender:  Optional[str] =None
    date_of_birth:  Optional[str] =None 
    marital_status:  Optional[str] =None  
    thread_id : Optional[str] =None
    document_number : Optional[str] =None  
    issue_date : Optional[str] =None  
    expiration_date : Optional[str] =None  
    place_of_birth : Optional[str] =None  

  
class DocumentExtractedDataCreate(BaseModel):
    document_type:  Optional[str] =None
    firstname:  Optional[str] =None
    lastname:  Optional[str] =None
    document_number: Optional[str] =None
    gender:  Optional[str] =None
    date_of_birth:  Optional[str] =None 
    date_of_issue:  Optional[str] =None
    date_of_expiration:  Optional[str] =None
    place_of_birth:  Optional[str] =None
    thread_id: Optional[str] = None

class CombinedDataCreate(BaseModel):  
    user_data: UserCreate  
    document_data: DocumentExtractedDataCreate  

# Pydantic models for the response  
class User_Info(BaseModel):  
    Country: str  
    Firstname: str  
    Lastname: str  
    Father_fullname: str  
    Gender: str  
    Date_of_Birth: str  
    Marital_Status: str  
  
class Document_Info(BaseModel):  
    Passport_No: str  
    Passport_Issue_Date: str  
    Passport_Expiry_Date: str  
    Place_Of_Birth: str  
  
class Comparator_Detail(BaseModel):  
    proofOfIdentity: str  
    UserProvided: str  
    PresentUploadedDocuments: str  
  
class Response_Model(BaseModel):  
    agentDetails: List[Dict[str, User_Info]]  
    docCollDetails: List[Dict[str, Document_Info]]  
    comparatorAgentDetails: List[Comparator_Detail] 