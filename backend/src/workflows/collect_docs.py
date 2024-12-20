import os
import pprint
import copy
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional , List, Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages.base import BaseMessage
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import AzureChatOpenAI
from loguru import logger
from pydantic import BaseModel, Field

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient, generate_container_sas, BlobSasPermissions

from src.models.agent_state import AgentState
from src.models.required_information import RequiredInformation
from src.models.doc_collector_state import DocCollectorState, Passport, SSN
from src.tool.document_tools import tools
from src.util.utils import trimmed_history, combine_required_info
from src.util.llm_singleton import LLMSingleton
from src.constants import Constant

load_dotenv()


llm = LLMSingleton().get_llm()


usa_assistant_prompt = """**Task**
You are a helpful assistant that helps with the KYC verification of users. Your job is to collet the documents from the user and then verify them.

**Information that needs to be collected from the user**
* Document : {doc_options} (User needs to choose which document they want to use. Do not display "None" as an option)


While collecting the information makesure to follow the following rules:
* The documents must be provided by the user compulsorily.
* The user can not proceed without proving the required information.
* If the asks to provide some random/invalid document that is not present on the list, the you must explain to the user that the document is invalid and ask them to provide the correct document.
* When the user asks to update the information, you must make sure to look at the current state and then answer the user whether the information was updated or not.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' STRICLY MARK THE USER CONFIRMATION AS 'TRUE'.
* You should collect all the necessary information and none of the field should be "None".

**Note** : If the user makes basic spelling mistakes (e.g., "passpotr" instead of "passport"), understand and process the input correctly
To track the state of all the steps you will be provided with the current state of the process:
{state}

Based on this state you must ask/answer the user.
* If the selected document fields are not filled you must ask the user to select the documents.
* If the selected document fileds are filled but check doc upload field is False, you must ask the user to uplod the documents again.
* If the information is present in the state, you MUST NOT ask the user to provide the information again.
"""

#TODO: Change for country wise
assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", usa_assistant_prompt),
        (
            "human",
            "The following is the history of the conversation till now: {history}",
        )
    ]
)


def doc_assistant_node(state):
    assistant_chain = assistant_prompt | llm
    res = assistant_chain.invoke(
        {
            "history": trimmed_history(state.history),
            "state": state.doc_collector_state,
            "doc_options": get_next_doc_to_collect(state.docs_to_collect)
        }
    )

    return {
        "history":[res],
        "output": [res]
    }


usa_collect_info_prompt = """You are an information collection agent. Your job is to look at the conversation and fill in the required information.
* You are to only make changes to the selected_doc1 field.
* Based on the user's response the value of the field can ONLY BE {doc_options}.
* Do not show "None" as the option when you are asking for {doc_options}.
* The user must explicitly state the name of the document they want to provide. Without explicit user input, the field should not be updated.
* If the user gives any value that is not SSN or Passport, the field should be updated to None.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'.
* You should collect all the necessary information and none of the field should be "None".
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.

**Note** : If the user makes basic spelling mistakes (e.g., "passpotr" instead of "passport"), understand and process the input correctly
"""

information_collection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", usa_collect_info_prompt),
        (
            "human",
            "The information collected so far: {collected_information}"
            "The following is the history of the conversation till now: {history}"
            "User Input: {user_input}"
        )
    ]
)


def doc_information_collection_node(state):
    llm_w_structured_output = llm.with_structured_output(DocCollectorState)
    information_stdin = state.user_input

    information_chain = information_collection_prompt | llm_w_structured_output

    res = information_chain.invoke({
        "doc_options":get_next_doc_to_collect(state.docs_to_collect),
        "history":trimmed_history(state.history),
        "collected_information": state.doc_collector_state,
        "user_input": information_stdin
    })
    print("RES:",res)


    # If user has selected the correct document
    if (res.selected_doc1 != None and res.selected_doc1 != "None") and res.doc1_information == None :
        # if globals()[res.selected_doc1]().__dict__.keys()!= res.doc1_information.keys():
        res.doc1_information = globals()[res.selected_doc1]().__dict__

    elif (res.selected_doc1 != None or res.selected_doc1 != "None") and res.doc1_information != None :
        if globals()[res.selected_doc1]().__dict__.keys()!= res.doc1_information.keys():
            res.doc1_information= globals()[res.selected_doc1]().__dict__
    res = DocCollectorState(**(combine_required_info(state.doc_collector_state,res)))
    print("UPDATED RES", res)

    return {"doc_collector_state":res,
            "history": [HumanMessage(content=information_stdin)],
            "output": [HumanMessage(content=information_stdin)]}


doc_upload_sys_prompt = """You are a document collector. Your job is to ask the user to upload the document.
The documents that you need to ask the are to be refered from the state of the process.
currently the user has selected the documents that they want to upload.
The current state of the process is provided below:
{state}

While asking the user to upload the document, just ask question similar to "Next, please proceed to upload **insert document name**"
The following are the steps that will be carried out during the process:
1) Document will be uploaded by the user.
2) A tool will check to see if the uploaded document was found in the azure blob and extract information from the document.
3) If in the state the value of the field if_doc1_uplaoded is False, you must ask the user to try and upload the document again.
4) Do not show "None" as the option when you are asking for upload documents.

"""


doc_upload_prompt = ChatPromptTemplate.from_messages([("system", doc_upload_sys_prompt),
                                                      ("human", "History of the conversation thus far: {history}")
                                                      ])

def doc_upload_assistant(state:AgentState):
    doc_upload_assistant_chain = doc_upload_prompt | llm
    res = doc_upload_assistant_chain.invoke(
        {"state": state.doc_collector_state, 
         "history":trimmed_history(state.history)})
    
    state_dict = state.doc_collector_state.__dict__
    state_dict.update({"if_doc1_uploaded":None})
    new_state = DocCollectorState(**state_dict) 

    return {"history":[res],
            "output":[res],
            "doc_collector_state": new_state}


# HITL break, wait for user to upload the document
def doc_upload(state:AgentState, config:RunnableConfig):
    # stdinput = state.user_input
    state_dict = state.doc_collector_state.__dict__
    state_dict.update({"if_doc1_uploaded":True})
    new_state = DocCollectorState(**state_dict)

    updated_flag = copy.deepcopy(state.flags)
    updated_flag.current_conversation_type = "upload"

    if new_state.if_doc1_uploaded == True:
        return {"doc_collector_state": new_state,
                "flags": updated_flag}
    else:
        return {"doc_collector_state": new_state,
                "flags": updated_flag}


# endpoint = os.environ.get("AZURE_DI_ENDPOINT")
# key = os.environ.get("AZURE_DI_KEY")
# blob_connection_string = os.environ.get("AZURE_BLOB_CONN_STRING")
container_name ="test"
account_name= "llmitdatastorage"

key_di = Constant.DI_KEY
# Initialize clients
document_analysis_client = DocumentAnalysisClient(
    endpoint=Constant.DI_API_ENDPOINT, 
    credential=AzureKeyCredential(key_di)
    )



def extract_passport_info(sas_url:str):
    extracted_information = {}
    confidence = 0

    try:
        res = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", document_url = sas_url)
        id_document_info = res.result().documents[0]

        extracted_information["DocumentType"] = id_document_info.doc_type  
        extracted_information["FirstName"] = id_document_info.fields.get('FirstName').value
        extracted_information["LastName"] = id_document_info.fields.get('LastName').value
        extracted_information["Sex"] = id_document_info.fields.get('Sex').value
        extracted_information["DocumentNumber"] = id_document_info.fields.get('DocumentNumber').value
        extracted_information["DateOfBirth"] = str(id_document_info.fields.get('DateOfBirth').value)
        extracted_information["DateOfIssue"] = str(id_document_info.fields.get('DateOfIssue').value)
        extracted_information["DateOfExpiration"] = str(id_document_info.fields.get('DateOfExpiration').value)
        extracted_information["PlaceOfBirth"] = id_document_info.fields.get('PlaceOfBirth').value
    
    except Exception as e:
        return "The Passport was not found in the Azure Blob. Please upload the document again."
    
    return extracted_information


def extract_ssn_info(sas_url:str):
    extracted_information = {}
    confidence = 0
    try:
        res = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", document_url = sas_url)
    except Exception as e:
        print(e)
        return "The SSN card was not found in the Azure Blob. Please upload the document again."
    id_document_info = res.result().documents[0]

    try:
        extracted_information["DocumentType"] = id_document_info.doc_type  
        extracted_information["FirstName"] = id_document_info.fields.get('FirstName').value
        extracted_information["LastName"] = id_document_info.fields.get('LastName').value
        extracted_information["DocumentNumber"] = id_document_info.fields.get('DocumentNumber').value

    except Exception as e:
        print("The Following Exception Occoured while extracting information from the Uploaded  SSN Document: ",e)
        return "Information could not be extracted from the document. Please try to upload the document again."
    
    return extracted_information


def extract_info(state:AgentState, config: RunnableConfig):
    map_dict = {"Passport":extract_passport_info, "SSN":extract_ssn_info}
    # UUID Extracted from config
    # FILE TYPE??
    user_uuid = str(config['configurable']['user_uuid'])
    print("UUID: ",user_uuid)

    # if state['doc_collector_state'].selected_doc1 == "Passport":
    #     blob_file_name = user_uuid+"-passport.png"
    #     extracted_information = map_dict[state['doc_collector_state'].selected_doc1](blob_file_name)
    
    # elif state['doc_collector_state'].selected_doc1 == "SSN":
    #     blob_file_name = user_uuid+"-ssn.png"
    #     extracted_information = map_dict[state['doc_collector_state'].selected_doc1](blob_file_name)

    # extracted_information = map_dict[state.doc_collector_state.selected_doc1](user_uuid+"-"+state.doc_collector_state.selected_doc1 + ".png")

    extracted_information = map_dict[state.doc_collector_state.selected_doc1](state.file_sas_url)
    print("EXTRACTED INFO: ",extracted_information)
    if type(extracted_information) != str:
        print("THE FOLLOWING INFORMATION WAS EXTRACTED FROM THE UPLOADED DOCUMENT: ",extracted_information) 

        if extracted_information == None:
            return {
                "history":[SystemMessage(content="The information could not be extracted from the document uploaded by the user. User is advised to try again.")],
                "output": [SystemMessage(content="The information could not be extracted from the document uploaded by the user. User is advised to try again.")],
                "doc_collector_state": None
                }

        else:
            state_dict = state.doc_collector_state.__dict__
            state_dict.update({"doc1_extracted_info":extracted_information,
                            "doc1_verification":True})
            new_state = DocCollectorState(**state_dict)
            return{
                "history":[SystemMessage(content="The information has been successfully extracted from the document uploaded by the user.")],
                "output":[SystemMessage(content="The information has been successfully extracted from the document uploaded by the user.")],
                "doc_info_history":[SystemMessage(content="The information has been successfully extracted from the document uploaded by the user.")],
                "doc_collector_state":new_state}
        
    else:
        print("There was trouble extracting the information from the document uploaded by the user. The user is advised to try again.")
        return {
            "history":[SystemMessage(content="There was trouble extracting the information from the document uploaded by the user. The user is advised to try again.")],
            "output":[SystemMessage(content="There was trouble extracting the information from the document uploaded by the user. The user is advised to try again.")],
            "doc_info_history":[SystemMessage(content="Could not extract information from the document uploaded by the user. Please try again.")]
        }

doc_info_collect_assistant_prompt = """You are an assistant whose job it is to collect the information regarding the document that the user has uploaded.(Keep in mind that the user has already uploaded the document.)  
The following is the information that needs to be collected.
{info_to_be_collected}

While collecting the information make sure to follow the following rules:
* All the information must be collected sequentially and one field at a time.
* It is compulsory to collect all the information mentioned above. No piece of information can be left out.
* Under no circumstances can the user proceed without providing the required information.
* If the user enters invalid information, you should explain the user why that input is wrong.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' STRICLY MARK THE USER CONFIRMATION AS 'TRUE'.
* You should collect all the necessary information and none of the field should be "None".
* If the user chooses to update the information, then you must ask which piece of information they would like to update and collect it accordingly.
* Whenever user updates information, ask for the confirmation of all details again. IT IS VITAL THAT THE INFORMATION RETRIEVED IS CORRECT.

The following information has been collected so far:
{current_state}
"""

doc_info_collector_system_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* Whenever the user wants to UPDATE or make correction to a field, ONLY THEN change that field to None.
* Once you have collected all the information you need to show all the information you have collected from the user and ask them if they want to update with the information that they have provided. ONLY THEN CAN YOU UPDATE THE user_confirmation field.
* If the user does not opt to change/update the value of any fields that they have entered, then you must STRICLY set the user_confirmation field to True.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

doc_info_collect_assistant_prompt = ChatPromptTemplate.from_messages([("system", doc_info_collect_assistant_prompt),
                                                           ("human", "History of the conversation so far: {doc_info_history}")])


doc_info_collector_prompt = ChatPromptTemplate.from_messages([("system", doc_info_collector_system_prompt),
                                                               ("human", "History of the conversation: {doc_info_history}")])

def collect_doc_info_assistant(state:AgentState):
    doc_info_collect_assistant_chain = doc_info_collect_assistant_prompt | llm  
    doc_info_to_be_collected = pprint.pformat(globals()[state.doc_collector_state.selected_doc1].model_json_schema()['properties'])

    res = doc_info_collect_assistant_chain.invoke(
        {
            "info_to_be_collected":doc_info_to_be_collected,
            "doc_info_history":trimmed_history(state.doc_info_history),
            "current_state": state.doc_collector_state.doc1_information
        }
    )
    return ({"doc_info_history":[res], "history":[res], "output":[res]})


def doc_info_collector(state:AgentState):
    llm_w_structured_output = llm.with_structured_output(globals()[state.doc_collector_state.selected_doc1])
    information_stdin = state.user_input
    doc_info_collector_chain = doc_info_collector_prompt | llm_w_structured_output
    hist_list = state.doc_info_history
    hist_list.append(HumanMessage(content=information_stdin))
    res = doc_info_collector_chain.invoke({
        "doc_info_history":trimmed_history(hist_list),
        "doc_collector_state": state.doc_collector_state.doc1_information
    })
    res = combine_required_info(state.doc_collector_state.doc1_information,res)


    state_dict = state.doc_collector_state.__dict__
    state_dict.update({"doc1_information":res})
    new_state = DocCollectorState(**state_dict)

    return (
        {   
            "doc_info_history":[HumanMessage(content=information_stdin)],
            "doc_collector_state": new_state,
            "history":[HumanMessage(content=information_stdin)],
            "output":[HumanMessage(content=information_stdin)],
            "doc_info_history":[HumanMessage(content=information_stdin)]
        }
    )


# function to extract which document to collect next 
def get_next_doc_to_collect(requried_docs):
    for doc in requried_docs:
        if doc['collected'] == False:
            return doc['doc']
    return None 

# Return the DocCollectorState pydantic class with correct literals for the documents in selected_doc1.
def update_doc_collector_state(required_docs: List):
    class DocCollectorState(BaseModel):
        selected_doc1: Optional[Literal[*required_docs]] = Field(
            description="The Document that the user chooses to provide for the KYC verification.", default=None
        )

        if_doc1_uploaded: Optional[bool] = Field(
            description="If user has uploaded the file.", default=None
        )

        doc1_information: Optional[dict]= Field(
            description="LLM SHOULD NOT UPDATE THIS FIELD. The field contains info about the uploaded document, provided by the user.", default=None
        )

        doc1_verification: Optional[bool]= Field(
            description="LLM SHOULD NOT UPDATE THIS FIELD. If the doc was successfully processed by DI.", default=None
        )

        doc1_extracted_info: Optional[dict] = Field(
            description="LLM SHOULD NOT UPDATE THIS FIELD. Information extracted by DI from the uploaded DOC.", default=None
        )
    
    return DocCollectorState


def init_doc_collector(state):
    required_docs = get_next_doc_to_collect(state.docs_to_collect)
    updated_state = update_doc_collector_state(required_docs)()
    doc_list = updated_state.model_json_schema()['properties']['selected_doc1']['anyOf'][0]['enum']
    if len(doc_list) ==2:
        mandatory_doc = None

        for i in doc_list:
            if i != "None":
                mandatory_doc = i
        updated_state.selected_doc1 = mandatory_doc

        if (updated_state.selected_doc1 != None and updated_state.selected_doc1 != "None") and updated_state.doc1_information == None :
            updated_state.doc1_information = globals()[updated_state.selected_doc1]().__dict__

    print("UPDATED DOC COLLECTOR INIT: ", updated_state)
    return {
        "doc_collector_state": updated_state,
        "history": [SystemMessage(content=f"The document collection process has been initiated for {required_docs}")],
        "output": [SystemMessage(content=f"The document collection process has been initiated for {required_docs}")]
    }


def update_docs_to_collect(state):
    updated_docs_to_collect = copy.deepcopy(state.docs_to_collect)
    for i in updated_docs_to_collect:
        if i["collected"] == False:
            i["collected"] = True
            break
    
    num_docs_left_to_collect = 0
    for i in updated_docs_to_collect:
        if i["collected"] == False:
            num_docs_left_to_collect +=1

    if num_docs_left_to_collect == 0:
        updated_flag = copy.deepcopy(state.flags)
        updated_flag.stepper = "3"
        return{
        "flags": updated_flag,
        "docs_to_collect": updated_docs_to_collect,
        "all_collected_docs": [state.doc_collector_state.__dict__]
    }
    
    return{
        "docs_to_collect": updated_docs_to_collect,
        "all_collected_docs": [state.doc_collector_state.__dict__]
    }