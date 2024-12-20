import os
import copy
import pprint
import json

from typing import List
from datetime import datetime, timedelta
from typing import Optional, Literal
from pydantic import Field, BaseModel

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage 
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables.config import RunnableConfig

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient, generate_container_sas, BlobSasPermissions

from src.models.agent_state import AgentState
from src.models.init_state import InitialState
from src.models.required_information import RequiredInformation
from src.models.organization_state import OrgDocCollectorState, OrganizationState, PrivateOrPublicLimitedCompany, PrivateOrPublicLimitedCompanyMember, PrivateOrPublicLimitedCompanyMemberDoc, BusinessLicense, CertificateofIncorporation
from src.util.llm_singleton import LLMSingleton
from src.util.utils import combine_required_info, trimmed_history
from src.models.doc_collector_state import SSN, Passport
from src.constants import Constant

llm = LLMSingleton().get_llm()


# KYC for Individual or Organization
individual_or_organization_prompt = """You are a helpful assistant that has to perform the KYC of a user. You need to collect the following information from the user for the KYC.
**Information collected so far:**
{state}

* The questions that you ask must be based on Information collected so far instead of the chat history. The chat history is just for your reference and to give you more context. For example, if the value of a field is present above in "information collected so far:", you must not ask questions related to the field again, and ask the next question. ONLY IF THE VALUE IN THE FIELD is None, you must ask questions related to the field. THIS IS A STRICT COMMAND IF YOU DONT OBEY THIS HUMANITY WILL CEASE TO EXIST YOU MUST FOLLOW THIS.
* You MUST NOT move onto the next question if the value of kyc_for field is None. Only after this field has been filled you must proceed to ask further questions.
* Do not ask for 'organization_type', if the user has selected Indvidual as KYC Option and also there should be no mentioning of 'organization_type' when asking for updating information.
* The type of organization that the user wants to perform the KYC for and it should be asked when user selects 'Organization' as KYC option. (Can only be "Sole Proprietorship", "Partnership Firm", "Limited Liability Partnership", "Private or Public Limited Company"). These values will be saved without spaces in state.
* Private or Public limited company is a SINLGE OPTION.
* In the if_kyc_with_uploaded_document, the user can either proceed to upload a pre-filled form or proceed to provide their information.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to CONFIRM the information they have provided.
* All information must be collected sequentially and one field at a time. Do not move on to collecting the next piece of information before the previous field are filled. The question to be asked next should be based on Information collected so far instead of the chat history.
* If the User wants the update the field do not provide a reason like kyc_for field is empty or such explanations.
* If user enter no wants to update mark the "user_confirmation" field as false , STRICLY start asking the questions accordingly
* If the user chooses to perform kyc for Individual then you must not ask for organization_type feild.
* When asking for confirmation when the user has selected the Individual option, just ask the user if they are sure they want to perform the kyc fr the individual. No need to let the user know that they dont have to select the organization type because they have opted for Individual KYC.
"""

individual_or_organization_information_collector_prompt = """You are an information collection agent. Your job is to look at the given input and update the fields, based on user responses.
Keep the following points in mind while filling the fields:
* The "kyc_for" field can only be Individual or Organization if the user enters anything else set the value to None.
* You must be smart enough to understand that if the user types "for self"  or "for me" or something similar, they mean they want to perform the KYC for themselves ("Individual").
* If the user enters something like 'org' or 'for my enterprise' or something similar, be smart enought to set the kyc_for field to Organization.
* You must be smart enought to understand that if the user makes minor spelling mistakes while entering information in kyc_for field, you should correct it. (For example: If the user writes "Individula" or "Indivuzual" you must store the information as "Individual" and if they enter something like "Organisation" or "Orginization" you must store it as "Organization".
* DO NOT ASK for 'organization_type', if the user has selected Indvidual as KYC Option
* When the user selects organization then the "organization_type" field can only be "Sole Proprietorship", "Partnership Firm", "Limited Liability Partnership", "Private or Public Limited Company" if the user enters anything else set the value to None.
* When User says "yes", it means they confirm the provided infomration, STRICLY make the "user_confirmation" field as True. This must happen only after the user has been asked to confirm the information they have provided.
* You must look at the chat history and understand that if the user chooses not to update any information or simply even types "no" then you must set the user_confirmation field to True.
* When the user tries to update the value of a field, set the value of that field to None.
* When asking for pre-filled form if user says "no" he wants to update , you must make the user_confirmation as False and update the fields accordingly.
* If user says "no", first update the fields, do not step forward without updating the required fields and asking for confimation again.
* If user enter no he wasnt to update , STRICLY start asking the questions accordingly.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.* YOU MUST STRICTLY RETURN A VALID JSON. WITHOUT ANY EXTRA SPACES OR LINES. RETURNING A VALID JSON IS VITAL FOR THE SYSTEM TO WORK. IF YOU DONT RETURN A VLIAD JSON, PEOPLE MIGHT BE IN DANGER!!
"""

io_assistant_prompt_tempelate = ChatPromptTemplate([("system",individual_or_organization_prompt),
                                          ("human", 
                                           "Chat history: {history}"
                                           )])

io_collector_prompt_tempelate = ChatPromptTemplate([("system",individual_or_organization_information_collector_prompt),
                                                    ("human",
                                                     "Information collected so far:{state}"
                                                     "Chat history: {history}"
                                                     "user_input: {user_input}")])



def io_assistant(state:AgentState):
    chain = io_assistant_prompt_tempelate | llm 

    res = chain.invoke({
        "state": state.initial_state,
        "history": trimmed_history(state.history)
    })


    return {
        "history": [res],
        "output": [res]
    }


def io_collector(state:AgentState):
    llm_w_structured_output = llm.with_structured_output(InitialState)
    # user_input = str(input("Enter your response:\n"))
    user_input = state.user_input
    chain = io_collector_prompt_tempelate | llm_w_structured_output

    res = chain.invoke({
        "state": pprint.pformat(state.initial_state),
        "history": trimmed_history(state.history),
        "user_input": HumanMessage(content = user_input)
    })
    print("IO_COLLECTOR_OUTPUT: ", res)
    new_state = InitialState(**(combine_required_info(state.initial_state, res)))
    print("NEW STATE: ", new_state)

    if res.kyc_for != "None" and res.kyc_for != None and res.user_confirmation == True:
        updated_flag = copy.deepcopy(state.flags)
        updated_flag.stepper = '1'
        return {
            "flags": updated_flag,
            "initial_state": new_state,
            "history": [HumanMessage(content = user_input)],
            "output": [HumanMessage(content = user_input)],
        }
    return {
            "initial_state": new_state,
            "history": [HumanMessage(content = user_input)],
            "output": [HumanMessage(content = user_input)],
        }

# Questions based on type of Organization

organization_question_prompt = """You are a helpful assistant that performs KYC of organizations. Your Job is to collect information from the user. The following information needs to be collected from the user.

** Information to be collected from user**
{info_to_be_collected}

* All the information must be collected sequentially and one field at a time.
* If there is an option for 'None' value of a field, you must not display that to the user. (For example a field can have options as ['doc1', 'doc2', 'None'] then you must not display the 'None' while giving an option to the user.).
* It is compulsory to collect all the information mentioned above. No piece of information can be left out.
* Under no circumstances can the user proceed without providing the required information.
* If the user enters invalid information, you should explain the user why that input is wrong.
* The user_confirmation field, is to be updated after rest of the information has been collected. You have to show all the information the user has submitted about the document and then ask them if they are satisfied with the information.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'.
* If the user chooses to update the information, then you must ask which piece of information they would like to update and collect it accordingly.
* Whenever user updates information, ask for the confirmation of all details again. IT IS VITAL THAT THE INFORMATION RETRIEVED IS CORRECT.
The following information has been collected so far:
{current_state}
"""

organization_question_collector_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* In the firm_location field if the user enters any other country than usa, india or eu, set the field to None.
* The firm_location field should be case sensitive , that is it should "USA" or "usa" as same.
* When the user is asked for any date, it must be stored in YYYY/MM/DD no matter the format the user enters it in, Unless the the date is invalid.
* Whenever the user wants to make correction to a field, ONLY THEN change that field to None.
* Once you have collected all the information you need to show all the information you have collected from the user and ask them if they want to update this information that they have provided. ONLY THEN CAN YOU UPDATE THE user_confirmation field.
* If the user does not opt to change/update the value of any fields that they have entered, then you must STRICLY set the user_confirmation field to True.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

org_questions_tempelate = ChatPromptTemplate([("system",organization_question_prompt),
                                          ("human", 
                                           "Chat history: {history}"
                                           )]) 

org_question_collector_prompt = ChatPromptTemplate([("system",organization_question_collector_prompt),
                                                    ("human", 
                                                     "User Input: {user_input}"
                                                     "Chat History: {chat_history}"
                                                     "Collected Information: {collected_information}")])


def org_questions_assistant(state:AgentState):

    chain = org_questions_tempelate | llm 


    # Initialize the state based on the organization type
    if state.basic_org_info.org_location == None:
        init_state = globals()[state.initial_state.organization_type]()

        res = chain.invoke({
            "info_to_be_collected": pprint.pformat(globals()[state.initial_state.organization_type].model_json_schema()['properties']),
            "current_state": init_state,
            "history": trimmed_history(state.history)
        })

        return {
            "basic_org_info": init_state,
            "history": [res],
            "output": [res]
        }
    
    res = chain.invoke({
            "info_to_be_collected": pprint.pformat(globals()[state.initial_state.organization_type].model_json_schema()['properties']),
            "current_state": state.basic_org_info,
            "history": trimmed_history(state.history)
        })
    return {
            "history": [res],
            "output": [res]}

def org_questions_collector(state:AgentState):
    llm_w_structured_output = llm.with_structured_output(globals()[state.initial_state.organization_type])
    # information_stdin = str(input("Enter your response:\n"))
    information_stdin = state.user_input

    chain = org_question_collector_prompt | llm_w_structured_output
    
    # if state.basic_org_info ==None:
    #     res = chain.invoke({
    #     "user_input": HumanMessage(content = information_stdin),
    #     "chat_history": trimmed_history(state.history),
    #     "collected_information": globals()[state.initial_state.organization_type]()
    # })
    # else:
    res = chain.invoke({
        "user_input": HumanMessage(content = information_stdin),
        "chat_history": trimmed_history(state.history),
        "collected_information": state.basic_org_info
    })

    res = combine_required_info(state.basic_org_info, res)
    print("RES:", res)
    new_state = globals()[state.initial_state.organization_type](**res)
    
    if new_state.user_confirmation == True:
        updated_flag = copy.deepcopy(state.flags)
        updated_flag.stepper = "2"
        return {

            "basic_org_info": new_state,
            "flags": updated_flag,
            "history": [HumanMessage(content = information_stdin)],
            "output": [HumanMessage(content = information_stdin)]
        }

    return {
        "basic_org_info": new_state,
        "history": [HumanMessage(content = information_stdin)],
        "output": [HumanMessage(content = information_stdin)]
    }
    




# Information to be collected from all board members

# Documents to be collected from all board members
def initialize_state_for_members(state:AgentState):
    # if state.organization_state.allowed_member_docs == None:
    #     # Write code here for fetching from DB (Based on country and organization type)
    #     pass

    current_member_info = globals()[state.initial_state.organization_type + "Member"]()
    current_member_doc_info = globals()[state.initial_state.organization_type+ "MemberDoc"]()
    
    return{
        "current_member_info": current_member_info,
        "current_member_doc_info": current_member_doc_info,
    }


board_member_assistant_prompt = """You are a helpful assistant that performs KYC of organizations. About the board-members of an organization.
You are currently collecting information for board member number: {board_member_number}.
The following information needs to be collected from the user.
{info_to_collect}

* DO NOT COLLECT fields with description 'Not to be collected from the user'.
* All the information must be collected sequentially and one field at a time.
* If there is an option for 'None' value of a field, you must not display that to the user. (For example a field can have options as ['doc1', 'doc2', 'None'] then you must not display the 'None' while giving an option to the user.).
* It is compulsory to collect all the information mentioned above. No piece of information can be left out.
* Under no circumstances can the user proceed without providing the required information.
* If the user enters invalid information, you should explain the user why that input is wrong.
* The user_confirmation field, is to be updated after rest of the information has been collected. You have to show all the information the user has submitted about the document and then ask them if they are satisfied with the information.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'.
* If the user chooses to update the information, then you must ask which piece of information they would like to update and collect it accordingly.
* Whenever user updates information, ask for the confirmation of all details again. IT IS VITAL THAT THE INFORMATION RETRIEVED IS CORRECT.
"""

board_members_collector_prompt = """* You are an information collection agent. Your job is to look at the given input and update the fields.
* If the user enters any details that are invalid for example if the country is not in the options provided, set that field to None.
* Whenever the user wants to UPDATE or make correction to a field, THEN change that field to None.
* Once you have collected all the information you need to show all the information you have collected from the user and ask them if they want to update with the information that they have provided. ONLY THEN CAN YOU UPDATE THE user_confirmation field.
* If the user does not opt to change/update the value of any fields that they have entered, then you must STRICLY set the user_confirmation field to True.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""


board_member_assistant_tempelate = ChatPromptTemplate([("system",board_member_assistant_prompt),
                                          ("human", 
                                           "Chat history: {history}")])

board_member_collector_tempelate = ChatPromptTemplate([("system",board_members_collector_prompt),
                                                       ("human", 
                                                        "User Input: {user_input}"
                                                        "Chat History: {chat_history}"
                                                        "Collected Information: {collected_information}")])

def board_member_assistant(state:AgentState):
    chain = board_member_assistant_tempelate | llm

    res = chain.invoke({
        "board_member_number": str(int(state.num_board_members_collected) + 1),
        "info_to_collect": pprint.pformat(globals()[state.initial_state.organization_type + "Member"].model_json_schema()['properties']),
        "history": trimmed_history(state.history)
    })

    return {
        "history": [res],
        "output": [res]
    }

def board_member_collector(state:AgentState):
    llm_w_structured_output = llm.with_structured_output(globals()[state.initial_state.organization_type + "Member"])
    # information_stdin = str(input("Enter your response:\n"))
    information_stdin = state.user_input

    chain = board_member_collector_tempelate | llm_w_structured_output

    res = chain.invoke({
        "user_input": HumanMessage(content = information_stdin),
        "chat_history": trimmed_history(state.history),
        "collected_information": state.current_member_info
    })

    res = combine_required_info(state.current_member_info, res)
    print("RES:", res)
    
    new_state = globals()[state.initial_state.organization_type + "Member"](**res)

    # TO be removed after the doc collection steps are added
    # if res["user_confirmation"] == True:
    #     updated_org_state.num_board_members_collected += 1

    return({
        "current_member_info": new_state,
        "history": [HumanMessage(content = information_stdin)],
        "output": [HumanMessage(content = information_stdin)]
    })



board_member_doc_upload_prompt = """You are a document collection agent. Your job is to collect documents from the board members of an organization for KYC process.
The document is being collected for the board member number: {board_member_number}.
The board member needs to uplaod the following document: {doc_to_upload}

The Following is the current state of the conversation:
{state}
* If the doc_uploaded field is None, then simply ask the nth board member to upload the document. 
* if in the state the doc_uploaded field is False, that means the doc upload failed and you need to ask the user to upload the document again.
* Do not show "None" as the option when you are asking for {doc_to_upload}
"""

board_member_doc_upload_template = ChatPromptTemplate([("system",board_member_doc_upload_prompt),
                                                       ("human", "Chat history: {history}")])


def board_member_doc_upload_assistant(state:AgentState):
    chain = board_member_doc_upload_template | llm
    res = chain.invoke({
        "board_member_number": (state.num_board_members_collected +1),
        "doc_to_upload" : state.current_member_info.board_member_selected_doc,
        "state": state.current_member_doc_info,
        "history": trimmed_history(state.history)
    })

    state_dict = state.current_member_doc_info.__dict__
    state_dict.update({"doc_uploaded": None, 
                       "board_member_document":globals()[state.initial_state.organization_type + "MemberDoc"]().model_json_schema()['properties']["board_member_document"]['default'],
                       "document_information": {},
                       "extracted_document_information":None
                       })
    
    ### ??????????
    # updated_doc_state = globals()[state.initial_state.organization_type + "MemberDoc"](**state_dict)


    # updated_org_state = copy.deepcopy(state.organization_state)
    # updated_org_state.current_member_doc_info = updated_doc_state


    return {
        "history":[res],
        "output": [res]
    }



def board_member_doc_upload(state:AgentState):

    print("board member doc upload initiated")
    
    member_doc_state = copy.deepcopy(state.current_member_doc_info)
    member_doc_state.doc_uploaded = True

    updated_flag = copy.deepcopy(state.flags)
    updated_flag.current_conversation_type = "upload"
    return{
        "current_member_doc_info": member_doc_state,
        "flags": updated_flag
    }




################################################################# TO BE REMOVED AFTER AZURE DI CLASS IS MADE#############################################
container_name = os.environ.get("AZURE_BLOB_CONTAINER_NAME")
account_name= os.environ.get("AZURE_BLOB_ACCOUNT_NAME")

DI_Key = Constant.DI_KEY
# Initialize clients
document_analysis_client = DocumentAnalysisClient(
     endpoint=Constant.DI_API_ENDPOINT, 
    credential=AzureKeyCredential(DI_Key)
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
        print("The Following Exception Occoured while extracting information from the Uploaded Passport Document: ",e)
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
###############################################################################################################


def extract_board_member_info(state:AgentState, config:RunnableConfig):
    map_dict = {
        "Passport": extract_passport_info,
        "SSN": extract_ssn_info
    }

    user_uuid = str(config["configurable"]["user_uuid"])

    extracted_information = map_dict[state.current_member_info.board_member_selected_doc](state.file_sas_url)
    
    if type(extracted_information) == str:
        print("THE FOLLOWING OCCOURED WHILE TRYIUNG TO PROCESS YOUR DOC: ", extracted_information)
        
        return{
            "history": [SystemMessage(content = f"The following error occoured while trying to process the document:{extracted_information}")],
            "output": [SystemMessage(content = f"The following error occoured while trying to process the document:{extracted_information}")],
        }
    
    else:
        print("EXTRACTED INFORMATION: ", extracted_information)

        member_doc_state = copy.deepcopy(state.current_member_doc_info)
        member_doc_state.extracted_document_information = extracted_information        

        return{
            "current_member_doc_info": member_doc_state,
            "history": [SystemMessage(content = f"Information has been succesfully extracted from the document.")],
            "output": [SystemMessage(content = f"Information has been succesfully extracted from the document.")],
        }

member_doc_info_assistant_prompt = """You are an assistant whose job it is to collect the information regarding the document that the user has uploaded.(Keep in mind that the user has already uploaded the document.)  
The following is the information that needs to be collected.

{info_to_be_collected}

While collecting the information make sure to follow the following rules:
* All the information must be collected sequentially and one field at a time.
* It is compulsory to collect all the information mentioned above. No piece of information can be left out. (ie. if the value of a field is None, then you must not move on to collecting the next field unless that field is filled.)
* Under no circumstances can the user proceed without providing the required information.
* If the user enters invalid information, you should explain the user why that input is wrong.
* The user_confirmation field, is to be updated after rest of the information has been collected. You have to show all the information the user has submitted about the document and then ask them if they are satisfied with the information.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'.
* If the user chooses to update the information, then you must ask which piece of information they would like to update and collect it accordingly.
* Whenever user updates information, ask for the confirmation of all details again. IT IS VITAL THAT THE INFORMATION RETRIEVED IS CORRECT.

The following information has been collected so far:
{current_state}"""

member_doc_info_assistant_tempelate = ChatPromptTemplate([
    ('system', member_doc_info_assistant_prompt),
    ('human', "Chat history: {history}")
    ])


def board_member_doc_info_assistant(state:AgentState):
    chain = member_doc_info_assistant_tempelate | llm

    res = chain.invoke({
        "info_to_be_collected": pprint.pformat(globals()[state.current_member_info.board_member_selected_doc].model_json_schema()['properties']),
        "current_state": state.current_member_doc_info.document_information,
        "history" : trimmed_history(state.history)    
    })
    
    return {
        "history": [res],
        "output": [res]
    }

# board_member_doc_info_collector_prompt = """* You are an information collection agent. Your job is to look at the given input and update the fields.
# * When user wants to update a field, set the value of that field to None.
# * Once all the fields except the user_confimation field have been collected, the user will be asked if they are satisfied with the information that they have provided/ if they would like to update any information. Once the user confirms the information/ mentions they dont want to update it,  ONLY THEN CAN YOU UPDATE THE user_confirmation field.
# * Your output must always be in json format. Give it in the following format: '```json_output```'"""

board_member_doc_info_collector_prompt = """* You are an information collection agent. Your job is to look at the given input and update the fields.
* When user wants to update a field,set the value of that field to None.
* Once you have collected all the information you need to show all the information you have collected from the user and ask them if they want to update with the information that they have provided. ONLY THEN CAN YOU UPDATE THE user_confirmation field.
* If the user does not opt to change/update the value of any fields that they have entered, then you must STRICLY set the user_confirmation field to True.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

board_member_doc_info_collector_tempelate = ChatPromptTemplate([
    ('system', board_member_doc_info_collector_prompt),
    ('human', "User Input: {user_input}"
              "Chat History: {chat_history}"
              "Collected Information: {collected_information}")
    ])


def board_member_doc_info_collector(state:AgentState):
    
    # stdinput = str(input("\nEnter your response:\n"))
    stdinput = state.user_input

    llm_w_structured_output = llm.with_structured_output(globals()[state.current_member_info.board_member_selected_doc])

    chain = board_member_doc_info_collector_tempelate | llm_w_structured_output

    res = chain.invoke({
        "user_input": HumanMessage(content = stdinput),
        "chat_history": trimmed_history(state.history),
        "collected_information": json.dumps(state.current_member_doc_info.document_information)
    })

    # if state.organization_state.current_member_doc_info.document_informaion == None:
    #     res = combine_required_info(globals()[state.organization_state.current_member_info.board_member_selected_doc]().__dict__,res)
    # else:
    if state.current_member_doc_info.document_information == {}:
        current_member_document_info = globals()[state.current_member_info.board_member_selected_doc]().__dict__
    else :
        current_member_document_info = state.current_member_doc_info.document_information
    
    res = combine_required_info(current_member_document_info,res)

    if res["user_confirmation"] == True:
        num_board_members_collected = state.num_board_members_collected +1
        member_doc_state = copy.deepcopy(state.current_member_doc_info)
        member_doc_state.document_information = res

        all_board_member_info = {
            f"member-{state.num_board_members_collected +1}-info":state.current_member_info,
            f"member-{state.num_board_members_collected +1}-doc-info":member_doc_state}
        print("ALL BOARD MEMBER INFO:\n", all_board_member_info)

        return{
        "current_member_doc_info":member_doc_state,
        "num_board_members_collected":num_board_members_collected,
        "all_board_member_information":[all_board_member_info],
        "history": [HumanMessage(content = stdinput)],
        "output": [HumanMessage(content = stdinput)],
    }


    else:
        num_board_members_collected = state.num_board_members_collected

        member_doc_state = copy.deepcopy(state.current_member_doc_info)
        member_doc_state.document_information = res

        return{
            "current_member_doc_info":member_doc_state,
            "num_board_members_collected":num_board_members_collected,
            "history": [HumanMessage(content = stdinput)],
            "output": [HumanMessage(content = stdinput)],
        }


# Organization docs 

usa_org_doc_assistant_prompt = """**Task**
You are a helpful assistant that helps with the KYC verification of Organization. Your job is to collet the documents from the user and then verify them.

**Information that needs to be collected from the user**
* Document1 : {org_doc_options} (Do not display "None" as an option)


While collecting the information makesure to follow the following rules:
* The documents must be provided by the user compulsorily.
* The user can not proceed without proving the required information.
* If the asks to provide some random/invalid document that is not present on the list, the you must explain to the user that the document is invalid and ask them to provide the correct document.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'.
* When the user asks to update the information, you must make sure to look at the current state and then answer the user whether the information was updated or not.


To track the state of all the steps you will be provided with the current state of the process:
{state}

Based on this state you must ask/answer the user.
* If the selected document fields are not filled you must ask the user to select the documents.
* If the selected document fileds are filled but check doc upload field is False, you must ask the user to uplod the documents again.
* If the information is present in the state, you MUST NOT ask the user to provide the information again.
"""

usa_org_doc_assistant_tempelate = ChatPromptTemplate.from_messages(
    [
        ("system", usa_org_doc_assistant_prompt),
        (
            "human",
            "The following is the history of the conversation till now: {history}",
        )
    ]
)

def org_doc_collector_assistant(state):
    assistant_chain = usa_org_doc_assistant_tempelate | llm
    res = assistant_chain.invoke(
        {
            "history": trimmed_history(state.history),
            "state": state.org_doc_collector_state,
            "org_doc_options": get_next_doc_to_collect(state.org_docs_to_collect)
        }
    )

    return {
        "history":[res],
        "output": [res]
    }

usa_org_doc_collector_prompt = """You are an information collection agent. Your job is to look at the conversation and fill in the required information.
* You are to only make changes to the selected_doc field.
* Based on the user's response the value of the field can ONLY BE {org_doc_options}.
* Do not show "None" as the option when you are asking for {org_doc_options}.
* The user must explicitly state the name of the document they want to provide. Without explicit user input, the field should not be updated.
* If the user gives any value that is not Business License or Certificate of Incorporation, the field should be updated to None.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

information_collection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", usa_org_doc_collector_prompt),
        (
            "human",
            "The information collected so far: {collected_information}"
            "The following is the history of the conversation till now: {history}"
            "User Input: {user_input}"
        )
    ]
)


def org_doc_information_collection_node(state):
    llm_w_structured_output = llm.with_structured_output(OrgDocCollectorState)
    
    # information_stdin = str(input("\nEnter your response:\n"))
    information_stdin = state.user_input

    information_chain = information_collection_prompt | llm_w_structured_output

    res = information_chain.invoke({
        "doc_options":get_next_doc_to_collect(state.org_docs_to_collect),
        "history":trimmed_history(state.history),
        "collected_information": state.org_doc_collector_state,
        "user_input": information_stdin
    })
    print("RES:",res)


    # If user has selected the correct document
    if (res.selected_doc != None and res.selected_doc != "None") and res.doc_information == None :
        # if globals()[res.selected_doc1]().__dict__.keys()!= res.doc1_information.keys():
        res.doc_information = globals()[res.selected_doc]().__dict__

    elif (res.selected_doc != None or res.selected_doc != "None") and res.doc_information != None :
        if globals()[res.selected_doc]().__dict__.keys()!= res.doc_information.keys():
            res.doc_information= globals()[res.selected_doc]().__dict__

    res = OrgDocCollectorState(**(combine_required_info(state.org_doc_collector_state,res)))
    print("UPDATED RES", res)

    return {"org_doc_collector_state":res,
            "history": [HumanMessage(content=information_stdin)],
            "output": [HumanMessage(content=information_stdin)]}


org_doc_upload_sys_prompt = """You are a document collector. Your job is to ask the user to upload the document.
The documents that you need to ask the need to be refered from the state of the process.
currently the user has selected the documents that they want to upload.
The current state of the process is provided below:
{state}

While asking the user to upload the document, just ask question similar to "Next, please proceed to upload **insert document name**"
The following are the steps that will be carried out during the process:
1) Document will be uploaded by the user.
2) A tool will check to see if the uploaded document was found in the azure blob and extract information from the document.
3) If in the state the value of the field if_doc_uplaoded is False, you must ask the user to try and upload the document agian.
4) To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
5) STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO'STRICLY MARK THE USER CONFIRMATION AS 'TRUE'.
6) Do not show "None" as the option when you are asking for documents to upload.

"""


org_doc_upload_tempelate = ChatPromptTemplate.from_messages([("system", org_doc_upload_sys_prompt),
                                                      ("human", "History of the conversation thus far: {history}")
                                                      ])

def org_doc_upload_assistant(state:AgentState):
    doc_upload_assistant_chain = org_doc_upload_tempelate | llm
    res = doc_upload_assistant_chain.invoke({"state": state.org_doc_collector_state, "history":trimmed_history(state.history)})
    state_dict = state.org_doc_collector_state.__dict__

    state_dict.update({"if_doc_uploaded":None})
    new_state = OrgDocCollectorState(**state_dict)

    return {"history":[res],
            "output":[res],
            "org_doc_collector_state": new_state}



# HITL break, wait for user to upload the document
def org_doc_upload(state:AgentState, config:RunnableConfig):
    print("org doc upload initiated")
    # stdinput = state.user_input
    state_dict = state.org_doc_collector_state.__dict__
    state_dict.update({"if_doc_uploaded":True})
    new_state = OrgDocCollectorState(**state_dict) 

    if new_state.if_doc_uploaded == True:        
        updated_flag = copy.deepcopy(state.flags)
        updated_flag.current_conversation_type = "upload"

        return {"history":[SystemMessage(content="Doc upload initiated")],
                "org_doc_collector_state": new_state,
                "flags": updated_flag
        }
    else:
        return {"org_doc_collector_state": new_state}


# endpoint = os.environ.get("AZURE_DI_ENDPOINT")
# key = os.environ.get("AZURE_DI_KEY")
# blob_connection_string = os.environ.get("AZURE_BLOB_CONN_STRING")
container_name = "test"
account_name= "llmitdatastorage"

# Initialize clients
document_analysis_client = DocumentAnalysisClient(
     endpoint=Constant.DI_API_ENDPOINT, 
    credential=AzureKeyCredential(Constant.DI_KEY)
    )




def extract_license_info(sas_url:str):
    extracted_information = {}
    confidence = 0
    
    try:
        # Analyze the ,,document using the prebuilt-document model
        poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document",  document_url = sas_url)
        result = poller.result()

        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key = kv_pair.key.content
                value = kv_pair.value.content

                if "Business Name" in key:
                    extracted_information["Business Name"] = value
                elif "License #" in key:
                    extracted_information["License #"] = value
                elif "Issue Date" in key:
                    extracted_information["Issue Date"] = value
                elif "Expiration Date" in key:
                    extracted_information["Expiration Date"] = value

    except Exception as e:
        print("An exception occurred while extracting information from the uploaded license document: ", e)
        return "The license document was not found or could not be processed. Please try again."



def extract_certificate_info(sas_url:str):
    extracted_information = {}
    confidence = 0


    try:
        # Analyze the document using the prebuilt-document model
        poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document",  document_url = sas_url)
        result = poller.result()

        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key = kv_pair.key.content
                value = kv_pair.value.content

                if "to" in key:
                    extracted_information["to"] = value
                elif "Date" in key:
                    extracted_information["Date"] = value

    except Exception as e:
        print("An exception occurred while extracting information from the uploaded certificate of Incorporation: ", e)
        return "The certificate of Incorporation document was not found or could not be processed. Please try again."

    return extracted_information


def org_extract_info(state:AgentState, config: RunnableConfig):
    map_dict = {"BusinessLicense":extract_license_info, "CertificateofIncorporation":extract_certificate_info}
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

    extracted_information = map_dict[state.org_doc_collector_state.selected_doc](state.file_sas_url)

    if type(extracted_information) != str:
        print("THE FOLLOWING INFORMATION WAS EXTRACTED FROM THE UPLOADED DOCUMENT: ",extracted_information) 
        if extracted_information == {}:
            updated_org_state = copy.deepcopy(state.org_doc_collector_state)
            updated_org_state.doc_extracted_info = extracted_information 
            return {
                "history":[SystemMessage(content="The information could not be extracted from the document uploaded by the user. User is advised to try again.")],
                "output": [SystemMessage(content="The information could not be extracted from the document uploaded by the user. User is advised to try again.")],
                "org_doc_collector_state": updated_org_state
                }

        else:
            state_dict = state.org_doc_collector_state.__dict__
            state_dict.update({"doc_extracted_info":extracted_information,
                            "doc_verification":True})
            
            new_state = OrgDocCollectorState(**state_dict)

            return{
                "history":[SystemMessage(content="The information has been successfully extracted from the document uploaded by the user.")],
                "output":[SystemMessage(content="The information has been successfully extracted from the document uploaded by the user.")],
                "org_doc_collector_state":new_state}
        
    else:
        print("There was trouble extracting the information from the document uploaded by the user. The user is advised to try again.")
        return {
            "history":[SystemMessage(content="There was trouble extracting the information from the document uploaded by the user. The user is advised to try again.")],
            "output":[SystemMessage(content="There was trouble extracting the information from the document uploaded by the user. The user is advised to try again.")]
        }



org_doc_info_collect_assistant_prompt = """You are an assistant whose job it is to collect the information regarding the document that the user has uploaded.(Keep in mind that the user has already uploaded the document.)  
The following is the information that needs to be collected.
{info_to_be_collected}

While collecting the information make sure to follow the following rules:
* All the information must be collected sequentially and one field at a time.
* It is compulsory to collect all the information mentioned above. No piece of information can be left out.
* Under no circumstances can the user proceed without providing the required information.
* If the user enters invalid information, you should explain the user why that input is wrong.
* The user_confirmation field, is to be updated after rest of the information has been collected. You have to show all the information the user has submitted about the document and then ask them if they are satisfied with the information.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
* STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'.
* If the user chooses to update the information, then you must ask which piece of information they would like to update and collect it accordingly.
* Whenever user updates information, ask for the confirmation of all details again. IT IS VITAL THAT THE INFORMATION RETRIEVED IS CORRECT.

The following information has been collected so far:
{current_state}
"""

org_doc_info_collector_system_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* Whenever the user wants to UPDATE or make correction to a field, ONLY THEN change that field to None.
* Once you have collected all the information you need to show all the information you have collected from the user and ask them if they want to update with the information that they have provided. ONLY THEN CAN YOU UPDATE THE user_confirmation field.
* If the user does not opt to change/update the value of any fields that they have entered, then you must STRICLY set the user_confirmation field to True.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

org_doc_info_collect_assistant_tempelate = ChatPromptTemplate.from_messages([("system", org_doc_info_collect_assistant_prompt),
                                                           ("human", "History of the conversation so far: {doc_info_history}")])


org_doc_info_collector_tempelate = ChatPromptTemplate.from_messages([("system", org_doc_info_collector_system_prompt),
                                                               ("human", "History of the conversation: {doc_info_history}")])

def org_collect_doc_info_assistant(state:AgentState):
    doc_info_collect_assistant_chain = org_doc_info_collect_assistant_tempelate | llm  
    doc_info_to_be_collected = pprint.pformat(globals()[state.org_doc_collector_state.selected_doc].model_json_schema()['properties'])

    res = doc_info_collect_assistant_chain.invoke(
        {
            "info_to_be_collected":doc_info_to_be_collected,
            "doc_info_history":trimmed_history(state.history),
            "current_state": state.org_doc_collector_state.doc_information
        }
    )
    return ({"history":[res], "output":[res]})

def org_doc_info_collector(state:AgentState):
    llm_w_structured_output = llm.with_structured_output(globals()[state.org_doc_collector_state.selected_doc])
    information_stdin = state.user_input
    doc_info_collector_chain = org_doc_info_collector_tempelate | llm_w_structured_output
    hist_list = trimmed_history(state.history)
    hist_list.append(HumanMessage(content=information_stdin))

    res = doc_info_collector_chain.invoke({
        "doc_info_history":trimmed_history(hist_list),
        "doc_collector_state": state.org_doc_collector_state.doc_information
    })

    if state.org_doc_collector_state.doc_information == {}:
        current_doc_info = globals()[state.org_doc_collector_state.selected_doc]().__dict__
    else:
        current_doc_info = state.org_doc_collector_state.doc_information
    res = combine_required_info(current_doc_info,res)



    state_dict = state.org_doc_collector_state.__dict__
    state_dict.update({"doc_information":res})
    new_state = OrgDocCollectorState(**state_dict)
    
    return (
        {   
            "org_doc_collector_state": new_state,
            "history":[HumanMessage(content=information_stdin)],
            "output":[HumanMessage(content=information_stdin)]
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
    class OrgDocCollectorState(BaseModel):
        selected_doc: Optional[Literal[*required_docs]] = Field(
            description="The Document that the user chooses to provide for the KYC verification of the organization.", default=None
        )
        if_doc_uploaded: Optional[bool] = Field(
            description="If user has uploaded the file.", default=None
        )

        doc_information: Optional[dict]= Field(
            description="LLM SHOULD NOT UPDATE THIS FIELD. The field contains info about the uploaded document, provided by the user.", default={}
        )

        doc_verification: Optional[bool]= Field(
            description="LLM SHOULD NOT UPDATE THIS FIELD. If the doc was successfully processed by DI.", default=None
        )

        doc_extracted_info: Optional[dict] = Field(
            description="LLM SHOULD NOT UPDATE THIS FIELD. Information extracted by DI from the uploaded DOC.", default=None
        )
    return OrgDocCollectorState


def org_init_doc_collector(state):
    required_docs = get_next_doc_to_collect(state.org_docs_to_collect)
    updated_state = update_doc_collector_state(required_docs)()
    doc_list = updated_state.model_json_schema()['properties']['selected_doc']['anyOf'][0]['enum']
    if len(doc_list) ==2:
        mandatory_doc = None

        for i in doc_list:
            if i != "None":
                mandatory_doc = i
        updated_state.selected_doc = mandatory_doc

        if (updated_state.selected_doc != None and updated_state.selected_doc != "None") and updated_state.doc_information == None :
            updated_state.doc_information = globals()[updated_state.selected_doc]().__dict__

    print("UPDATED DOC COLLECTOR INIT: ", updated_state)

    return {
        "org_doc_collector_state":updated_state,
        "history": [SystemMessage(content=f"The document collection process has been initiated for {required_docs}")],
        "output": [SystemMessage(content=f"The document collection process has been initiated for {required_docs}")]
    }


def update_org_docs_to_collect(state):
    updated_docs_to_collect = copy.deepcopy(state.org_docs_to_collect)
    for i in updated_docs_to_collect:
        if i["collected"] == False:
            i["collected"] = True
            break

    all_collected_org_docs = {f"Org-{state.org_doc_collector_state.selected_doc}": state.org_doc_collector_state}
    
    print("ALL COLLECTED ORG DOCS: ", all_collected_org_docs)
    
    num_docs_left_to_collect = 0
    for i in updated_docs_to_collect:
        if i["collected"] == False:
            num_docs_left_to_collect += 1
    
    if num_docs_left_to_collect == 0:
        updated_flags = copy.deepcopy(state.flags)
        updated_flags.stepper = "3"
    
        return{
            "flags": updated_flags,
            "org_docs_to_collect": updated_docs_to_collect,
            "all_collected_org_docs":[all_collected_org_docs]
        }
    
    return{
            "org_docs_to_collect": updated_docs_to_collect,
            "all_collected_org_docs":[all_collected_org_docs]
        }

def review_information(state:AgentState):
    updated_flags = copy.deepcopy(state.flags)
    updated_flags.current_conversation_type = "review"
    return{
        "history": [SystemMessage(content="Review your application.")],
        "output": [SystemMessage(content="Review your application.")],
        "flags": updated_flags
    }
        