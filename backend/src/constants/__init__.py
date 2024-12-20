import os
from urllib.parse import quote

from redis import Redis
class Constant:
    ASSISTANT = "assistant"
    COLLECT_INFO = "collect_info"
    GUIDELINES_FETCHER = "guidelines_fetcher"
    SAVE_INFO = "save_to_db"
    COLLECT_DOCS = "doc_collector"
    DOC_TOOLS = "doc_tools"
    PEP_EXTRACTOR= "pep_extractor"
    PEP_INFO="pep_assistant"
    PEP_COLLECT_INFO="pep_collection"
    DOC_ASSISTANT = "doc_assistant"
    COLLECT_DOC_INFO = "collect_doc_info"
    DOC_UPLOAD = "doc_upload"
    DOC_UPLOAD_ASSISTANT = "doc_upload_assistant"
    DOC_INFO_ASSISTANT = "doc_info_assistant"
    DOC_INFO_COLLECTOR = "info_collector"
    EXTRACT_INFO_FROM_DOC = "extract_info"
    INIT_DOC_COLLECTOR = "Doc_collector_init"
    UPDATE_DOCS_TO_COLLECT = "update_docs_to_collect"
    IO_ASSISTANT = "IO_assistant"
    IO_COLLECTOR = "IO_collector"

    # ORG member info collection
    ORG_QUES_ASSISTANT = "org_ques_assistant"
    ORG_QUES_COLLECTOR = "org_ques_collector"
    ORG_INIT_MEMBER_STATE = "init_member_state"
    ORG_MEMBER_QUES_ASSISTANT = "board_member_assistant"
    ORG_MEMBER_QUES_COLLECTOR = "board_member_collector"
    ORG_MEMBER_DOC_UPLOAD_ASSISTANT = "board_member_doc_upload_assistant"
    ORG_MEMBER_DOC_UPLOAD = "board_member_doc_upload"
    ORG_MEMBER_EXTRACT_INFO = "extract_member_info"
    ORG_MEMBER_DOC_INFO_ASSISTANT = "board_member_doc_info_assistant"
    ORG_MEMBER_DOC_INFO_COLLECTOR = "board_member_doc_info_collector"
    ORG_PEP_EXTRACTOR= "org_pep_extractor"
    ORG_PEP_INFO="org_pep_assistant"
    ORG_PEP_COLLECT_INFO="org_pep_collection"

    # ORG doc collection
    ORG_DOC_COLLECTOR_ASSISTANT = "org_doc_assistant"
    ORG_COLLECT_DOC_INFO = "org_collect_doc_info"
    ORG_DOC_UPLOAD = "org_doc_upload"
    ORG_DOC_UPLOAD_ASSISTANT = "org_doc_upload_assistant"
    ORG_DOC_INFO_ASSISTANT = "org_doc_info_assistant"
    ORG_DOC_INFO_COLLECTOR = "org_doc_info_collector"
    ORG_EXTRACT_INFORMATION = "org_extract_info"
    INIT_ORG_DOC_COLLECTOR = "org_doc_collector_init"
    UPDATE_ORG_DOCS_TO_COLLECT = "org_update_docs_to_collect"
    REVIEW_INFO = "review_information"
    
    # Pre-filled form
    UPLOAD_FILLED_FORM = "upload_filled_form"
    EXTRACT_INFO_FROM_FORM = "extract_info_from_form"
    UPDATE_EXTRACTED_INFO_ASSISTANT ="update_extracted_info_assistant"
    UPDATE_EXTRACTED_INFO_COLLECTOR = "update_extracted_info_collector"
    UPDATE_STATE_FROM_FORM = "update_state_from_form"
    FORM_DOC_UPLOAD_ASSISTANT = "form_doc_upload_assistant"
    UPLOAD_FORM_DOCS = "upload_form_docs"
    EXTRACT_INFO_FROM_FORM_DOC = "extract_info_from_form_doc"
    FORM_COLLECTOR_INIT = "initialize_form_collector"
    UPDATE_STATE_WITH_CONFIRMED_INFORMATION = "update_state_with_confirmed_information"

    COMPARATOR = "compare_info"
    ORG_COMPARATOR= "verify_org_kyc"
    CONTEXT_PATH ="/LLM-IT"
    # postgres will work on docker as image, no changes needed.
    POSTGRES_CONFIG={  
        'user': 'postgres',  
        'password': 'root',  
        'host': 'pgdb',  
        'port': '5432',  
        'dbname': 'LLM-IT'  
    }  
   
    #add connection string  and parameters
    CONNECTION_STRING = "<Blob-Conn-String>"
    CONTAINER_NAME = "<Blob-container-name>"
    ACCOUNT_NAME = "<Blob-account-name>"

# Redis will work on docker as image, no changes needed.
    REDIS_CONN= Redis(
        host="redis",
        port=6379,
        decode_responses=False,
        retry_on_timeout=True

) 
    SECRET_KEY = "hwvYo/vRkShexkRC0pz7ak1qga/3WSecZhZxKQfYLKY=" #key for encryption and no need to change this

    '''add necessary API keys ,Endpoints and deployment name for
       specific resource. '''
    GPT4_TURBO_KEY = "<Enter-Your-Key>"
    GPT4o_KEY = "<Enter-Your-Key>"
    EMBEDDING_KEY = "<Enter-Your-Key>"
    DI_KEY = "<Enter-Your-Key>"
    GPT4o_API_ENDPOINT = "<Enter-Your-KEY>"
    GPT4_TURBO_ENDPOINT = "<Enter-Your-Key>"
    EMBEDDING_API_ENDPOINT = "<Enter-Your-KEY>"
    DI_API_ENDPOINT = "<Enter-Your-KEY>"
    AZURE_4o_DEPLOYMENT_NAME  = "<Enter-Your-KEY>"
    AZURE_4_TURBO_DEPLOYMENT_NAME = "<Enter-Your-KEY>"
    EMBEDDING_DEPLOYMENT_NAME = "<Enter-Your-KEY>"
   