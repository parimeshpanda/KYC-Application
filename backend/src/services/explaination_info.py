from base64 import b64decode
from datetime import datetime
from src.constants import Constant
from src.models.model import DocumentExtractedData, UserExtractedData
from src.schemas.user_extracted_data import DocumentExtractedDataCreate, UserCreate
from sqlalchemy.orm import Session  
from src.services.aes_util import encrypt_data
from src.workflows.workflow import graph
from datetime import datetime  
from src.schemas.user_extracted_data import DocumentExtractedDataCreate, UserCreate   


SECRET_KEY = b64decode(Constant.SECRET_KEY) 
def create_user_extracted_data(user_data: UserCreate, db: Session):  
    db_user = UserExtractedData(  
        country=user_data.country,  
        firstname=encrypt_data(SECRET_KEY, user_data.firstname),  
        lastname=encrypt_data(SECRET_KEY, user_data.lastname),  
        father_fullname=encrypt_data(SECRET_KEY, user_data.father_fullname),  
        gender=encrypt_data(SECRET_KEY, user_data.gender),  
        date_of_birth=encrypt_data(SECRET_KEY, user_data.date_of_birth),  
        marital_status=encrypt_data(SECRET_KEY, user_data.marital_status),  
        thread_id= user_data.thread_id,  
        time_stamp=datetime.now()  ,
        document_number = encrypt_data(SECRET_KEY, user_data.document_number),
        issue_date = encrypt_data(SECRET_KEY, user_data.issue_date),
        expiration_date = encrypt_data(SECRET_KEY, user_data.expiration_date),
        place_of_birth = encrypt_data(SECRET_KEY, user_data.place_of_birth)  ,
       

    )  
    db.add(db_user)  
    db.commit()  
    db.refresh(db_user)  
    return db_user  
  
def create_document_extracted_data(document_data: DocumentExtractedDataCreate, db: Session):  
    db_document = DocumentExtractedData(  
        document_type=document_data.document_type  ,
        firstname=encrypt_data(SECRET_KEY,document_data.firstname ),
        lastname=encrypt_data(SECRET_KEY,document_data.lastname ),
        document_number=encrypt_data(SECRET_KEY,document_data.document_number)  ,
        date_of_birth=encrypt_data(SECRET_KEY,document_data.date_of_birth ),
        date_of_issue=encrypt_data(SECRET_KEY,document_data.date_of_issue ),
        date_of_expiration=encrypt_data(SECRET_KEY,document_data.date_of_expiration) , 
        place_of_birth=encrypt_data(SECRET_KEY,document_data.place_of_birth ),
        gender=encrypt_data(SECRET_KEY,document_data.gender) , 
        thread_id=document_data.thread_id,  
        time_stamp=datetime.now()  # Add the current timestamp  
    )  
    db.add(db_document)  
    db.commit()  
    db.refresh(db_document)  
    return db_document  




  
def compare_info_individual( thread_id:str,db: Session):  
    config = {  
            "configurable": {  
                "user_uuid": 123123,  
                "thread_id": thread_id,  
                "checkpoint_ns": ""  
            },  
            "recursion_limit": 100,  
        }  
    state = graph.get_state(config).values
    personal_info = {  
        "First Name": state['user_information'].user_first_name,  
        "Last Name": state['user_information'].user_last_name,  
        "Date of Birth": state['user_information'].user_date_of_birth,  
        "Fathers Name": state['user_information'].user_father_name,  
        "Gender": state['user_information'].user_gender,  
        "Marital Status": state['user_information'].user_marital_status,  
        "User Country": state['user_information'].user_country  
    }    

    doc1_info = {}
    doc1_doc_type = state['doc_collector_state'].selected_doc1
    if doc1_doc_type == 'Passport':
        doc1_info['document_number'] = state['doc_collector_state'].doc1_information['passport_number']
        doc1_info['passport_issue_date'] = state['doc_collector_state'].doc1_information['passport_issue_date']
        doc1_info['passport_expiration_date'] = state['doc_collector_state'].doc1_information['passport_expiry_date']
        doc1_info['place_of_birth'] = state['doc_collector_state'].doc1_information['place_of_birth']
    elif doc1_doc_type == 'SSN':
        doc1_info['document_number'] = state['doc_collector_state'].doc1_information['ssn_number']
    
    
    # if state['pep_information'].pep_extracted_db:  
    #     personal_info["Political Exposure"] = state['pep_information'].pep_extracted_db  
    #     personal_info["Political person Input"] = state['pep_information'].political_exposure  
    #     personal_info["Bank Account Number"] = state['pep_information'].bank_acc_no  
    #     personal_info["Credit Score"] = state['pep_information'].credit_score  
  
    collected_doc_info = state['doc_collector_state'].doc1_extracted_info  
  
    if collected_doc_info:  
        if collected_doc_info['DocumentType'] == 'idDocument.usSocialSecurityCard':  
            collected_doc_info['DocumentType'] = 'Social Security Card'  
        elif collected_doc_info['DocumentType'] == 'idDocument.passport':  
            collected_doc_info['DocumentType'] = 'Passport'  
            collected_doc_info['DateOfBirth'] = collected_doc_info['DateOfBirth']  
            collected_doc_info['DateOfIssue'] = collected_doc_info['DateOfIssue']  
            collected_doc_info['DateOfExpiration'] = collected_doc_info['DateOfExpiration']  
            collected_doc_info['PlaceOfBirth'] = collected_doc_info['PlaceOfBirth']  
       
        user_data = UserCreate(  
            firstname=personal_info["First Name"],  
            lastname=personal_info["Last Name"],  
            father_fullname=personal_info["Fathers Name"],  
            gender=personal_info["Gender"],  
            date_of_birth=personal_info["Date of Birth"],  
            marital_status=personal_info["Marital Status"],  
            country=personal_info["User Country"],  
            thread_id=thread_id ,
            document_number = doc1_info["document_number"],
            issue_date = doc1_info.get("passport_issue_date") if doc1_info.get("passport_issue_date") else None,
            expiration_date = doc1_info.get("passport_expiration_date") if doc1_info.get("passport_expiration_date") else None,
            place_of_birth = doc1_info.get("place_of_birth")  if doc1_info.get("place_of_birth") else None
        )  
        create_user_extracted_data(user_data, db)  
  
        document_data = DocumentExtractedDataCreate(  
            document_type=collected_doc_info['DocumentType'],  
            firstname=collected_doc_info['FirstName'],  
            lastname=collected_doc_info['LastName'],  
            document_number=collected_doc_info['DocumentNumber'],  
            date_of_birth=collected_doc_info.get('DateOfBirth'),  
            date_of_issue=collected_doc_info.get('DateOfIssue'),  
            date_of_expiration=collected_doc_info.get('DateOfExpiration'),  
            place_of_birth=collected_doc_info.get('PlaceOfBirth'),  
            gender=collected_doc_info.get('Gender', personal_info["Gender"]),  
            thread_id=thread_id  
        )  
        create_document_extracted_data(document_data, db)  