import os
import copy
import pprint
import json

from typing import List
from datetime import datetime, timedelta
from typing import Optional, Literal
from pydantic import Field, BaseModel
from openai import AzureOpenAI


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage 
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langchain.output_parsers import PydanticOutputParser


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient, generate_container_sas, BlobSasPermissions

from src.models.agent_state import AgentState, APIFlags, UnifiedUserInformation
from src.models.init_state import InitialState
from src.models.doc_collector_state import DocCollectorState
from src.models.required_information import RequiredInformation
from src.models.organization_state import OrgDocCollectorState, OrganizationState, PrivateOrPublicLimitedCompany, PrivateOrPublicLimitedCompanyMember, PrivateOrPublicLimitedCompanyMemberDoc, BusinessLicense, CertificateofIncorporation
from src.util.llm_singleton import LLMSingleton
from src.util.utils import combine_required_info, trimmed_history, get_next_doc_to_collect
from src.models.doc_collector_state import SSN, Passport
from src.constants import Constant


llm = LLMSingleton().get_llm()

openai_client = AzureOpenAI(
    azure_endpoint= Constant.GPT4o_API_ENDPOINT,  # or your deployment
    api_version="2024-08-01-preview",  # or your api version
    azure_deployment=Constant.AZURE_4o_DEPLOYMENT_NAME,
    # api_key=client.get_secret("GPT-4o-API-KEY").value
    api_key= Constant.GPT4o_KEY
)

def call_azure_openai(prompt, image_data_url, client, aoai_deployment_name=Constant.AZURE_4o_DEPLOYMENT_NAME, response_format=None):  
    """  
    Call the Azure OpenAI service to analyze an image.  
    """  
    if response_format is None:  
        response = client.chat.completions.create(  
            model=aoai_deployment_name,  
            messages=[  
                {  
                    "role": "system",  
                    "content": "You are an AI helpful assistant."  
                },  
                {  
                    "role": "user",  
                    "content": [  
                        {  
                            "type": "text",  
                            "text": prompt  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": image_data_url  
                            }  
                        }  
                    ]  
                }  
            ],  
            max_tokens=4000,  
            temperature=0  
        )  
    else:  
        response = client.beta.chat.completions.parse(  
            model=aoai_deployment_name,  
            messages=[  
                {  
                    "role": "system",  
                    "content": "You are an AI helpful assistant."  
                },  
                {  
                    "role": "user",  
                    "content": [  
                        {  
                            "type": "text",  
                            "text": prompt  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": image_data_url  
                            }  
                        }  
                    ]  
                }  
            ],  
            max_tokens=4000,  
            temperature=0,  
            response_format=response_format  
        )  
      
    # Extract the content from the response  
    result = response.choices[0].message.content  
      
    # Return the result  
    return result

class DocumentList(BaseModel):
  document_list: List[Literal["SSN","Passport","Adhaar"]] = Field(description="List of documents present in the doucment")


# Interrupt after
def upload_filled_form(state):
  updated_flags = copy.deepcopy(state.flags)
  updated_flags.stepper = "1"
  updated_flags.current_conversation_type = "upload"
  return {
      "flags":updated_flags,
      "output": [SystemMessage(content="Please proceed to upload the filled form of the user you want to perform the KYC for.")]
  }

# Add in state a list w
extract_infor_from_form_prompt = """Your job is to provide a proper JSON response from the following document by analysing a proper document. 
* You need to provide me output of only following fields mentioned in the prompt  
* You need to collect the following fields is kyc_for an Individual or Organization.  
* Is the application_type new or old.  
* Personal details like first_name, last_name, gender, father_name, mother_name, date_of_birth, married_status, citizenship, residential_status  
* You have to check out for the list of documents that is provided in proof of identity and store in document_list  
* If the list contain passport , you need to have passport_number, date_of_issue, date_of_expiry  
* If the list contains SSN , you need to extract SSN_Number from the document.  
* You also need to extract complete address in one field as place_of_birth and it should be handled carefully when extracting from handwritten document.  
* Do not miss out on any information , Everything should be in proper JSON format. 
* For handwritten document, kindly review every information very carefully and then extract the correct information.
* Information like date_of_birth, passport_number, ssn_number, date_of_issue and date_of_expiry should be handled very carefully when extracting from handwritten document
""" 
  
def extract_info_from_filled_form(state):
    sas_url = state.file_sas_url
  # LLM EXTRACT INFO CODE, TO BE ADDED HERE

    result = call_azure_openai(extract_infor_from_form_prompt, sas_url, openai_client)

    print("The following information was extracted from the filled form: ", result)
    return{
      "filled_form_extracted_info": result,
      "history": [SystemMessage(content="The information has been extracted from the filled form.")]
  }


update_extracted_form_info_assistant_prompt = """You are a helpful assistant that has to perform the KYC of a user. You need to help the user validate the following information.
The following information has been collected from an user uploaded form. You need to help the user validate/update the information.

* You must always show the user whatever information has been collected, before asking them what field they want to update.
* If the user wants to update a field, you must ask them for the new value of the field.
* If the value of a field is 'None', it means that the information needs to be collected from the user. You must ask a question to the user asking for the information on the field/ ask for updated information on the field.
* After every update you must show the collected information to the user and ask if they are satisfied or not. If the user chooses not satisfied, they will be allowed to update the fields again.
* Make sure not to display the 'user_confirmation' field and 'user_country_updation' field to the user.
* If user does not fill ssn_number, passport_number, passport_issue_date, passport_expiry_date do not ask for the same, and do not show that ssn_number, passport_number, passport_issue_date, passport_expiry_date is none while showing all the information.
* INCLUDE THE DATE FORMAT AS DD/MM/YYYY besides the user entered information when showing the fields user_date_of_birth, user_passport_issue_date and user_passport_expiry_date for the user to update. THIS MUST BE STRICTLY FOLLOWED!!
* Make sure to display ALL THE FIELDS WHICH ARE NOT NONE (THIS IS VERY IMPORTANT AS INFORMATION NEEDS TO BE CONFIRMED FROM THE USER). DO NOT DISPLAY THE FIELDS WHICH ARE NONE.
* STRICLY ASK A 'YES' OR 'NO' QUESTION FOR CONFIRMING THE FINAL FIELD 'user_confirmation' , and if user says 'no' update the fields accordingly.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to CONFIRM the information they have provided.

**Schema/ Details of all the fields:**
{schema}

**The following information has been extracted from the uploaded document:**
{extracted_info}"""

update_extracted_form_info_collector_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* For the 'user_confirmation' field, the user must confirm the informatoin collected by saying yes. When the user says yes, update the field to True, else update the field to False.
* When the user wants to update a field/make correction to a field, set the field to "None".
* Whenever the user provides any date that is to be saved in a field, the date should be stored in YYYY/MM/DD format.
* You must never fill in any fields on your own. Only update the fields that the user wants to update, with the value they want to update it with.
* Whenever the user wants to UPDATE or MAKE CORRECTION to a field, ONLY THEN change that field to 'None'.
* DO NOT RETURN ANY SPACES BEFORE THE JSON OUTPUT!!!

* When User says "yes", it means they confirm the provided infomration, STRICLY make the "user_confirmation" field as True. This must happen only after the user has been asked to confirm the information they have provided.
* When the user ask for updating information, ask for the "user_confirmation" again and then only proceed ahead.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

update_extracted_form_info_assistant_prompt_template = ChatPromptTemplate([("system", update_extracted_form_info_assistant_prompt),
                                                                           ("human", "Chat History: {chat_history}")])

update_extracted_form_info_collector_prompt_template =  ChatPromptTemplate([("system", update_extracted_form_info_collector_prompt),
                                                                           ("human", 
                                                                            "Collected Information:\n {collected_information}"
                                                                            "Chat History: {chat_history}"
                                                                            "User Input: {user_input}")])

def update_extracted_form_info_assistant(state:AgentState):
    chain = update_extracted_form_info_assistant_prompt_template | llm

    res = chain.invoke({
       "schema":pprint.pformat(UnifiedUserInformation.model_json_schema()['properties']),
       "extracted_info": pprint.pformat(state.filled_form_extracted_structured_info),
       "chat_history":trimmed_history(state.history)})
    
    return{
        "output":[res],
        "history":[res]
    }

# Interrupt before
def update_extracted_form_info_collector(state:AgentState):
    # llm_w_struct = llm.with_structured_output(UnifiedUserInformation)
    # chain = update_extracted_form_info_collector_prompt_template |llm_w_struct
    parser = PydanticOutputParser(pydantic_object=UnifiedUserInformation)
    chain = update_extracted_form_info_collector_prompt_template |llm | parser

    print("\n\n\n")
    for i in state.history:
        print(i.content)
    res = chain.invoke({
        "collected_information": pprint.pformat(state.filled_form_extracted_structured_info),
        "chat_history":pprint.pformat(trimmed_history(state.history)),
        "user_input":state.user_input
    })
    
    updated_res = combine_required_info(state.user_information, res)
    updated_unified_info = UnifiedUserInformation(**updated_res)

    return{
        "history":[HumanMessage(content=state.user_input )],
        "output":[HumanMessage(content=state.user_input )],
        "filled_form_extracted_structured_info": updated_unified_info,
    }

def update_state_from_final_information(state):
        # LLM output in the document structure
        llm_w_struct = llm.with_structured_output(RequiredInformation)

        confirmed_user_information = llm_w_struct.invoke(pprint.pformat(state.filled_form_extracted_structured_info))
        
        return {
            "user_information": confirmed_user_information,
            "history":[SystemMessage(content="The information has been confirmed by the user and saved into the state.")]
        }


def update_state_from_extracted_info(state):
    # To be fetched from state.filled_form_extracted_info
    extracted_info = state.filled_form_extracted_info
    if state.initial_state.kyc_for == "Individual":
      # Extracting information and updating the state
      llm_w_required_info_structure = llm.with_structured_output(UnifiedUserInformation)
      filled_form_extracted_structured_info = llm_w_required_info_structure.invoke(pprint.pformat(extracted_info))

    print("STRUCTURED OUTPUT:\n",filled_form_extracted_structured_info)
    # Extracting List of documents mentioned by the user.
    llm_w_doc_list_structure = llm.with_structured_output(DocumentList)
    document_list = llm_w_doc_list_structure.invoke(pprint.pformat(extracted_info))


    updated_docs_to_collect = []
    for i in document_list.document_list:
      updated_docs_to_collect.append({"doc":[i,"None"], "collected":False})
          

      # TO BE ADDED LATER FOR ORGANIZATION
      # elif state.initial_state.kyc_for =="Organization":
      #     pass
          

    return {
      "filled_form_extracted_structured_info": filled_form_extracted_structured_info,
      "flags": APIFlags(current_conversation_type="conversation", stepper = "1"),
      "docs_to_collect": updated_docs_to_collect
  }



form_doc_assistant_prompt = """You are an assistant whose job it is to collect the required documents for the KYC of the individual. The user has already uploaded a copy of the filled KYC form.
Now it is your job to ask for the documents supporting the information provided in the form.

You need to collect the following document from the user:
{doc_to_collect} (Make sure you ask for the correct document)

It might be so that the user uploads a differnt document that the one asked above. In that case, you need to ask the user for the correct document.
To check if the user has uploaded correct document, you must refer to the errors below.

Errors while uploading the document:
{state}

If the errors are empty, it means the user has uploaded the correct document. If some error is present the user has uploaded wrong document and you must ask the user to reupload.
"""

form_doc_assistant_prompt_template = ChatPromptTemplate([("system", form_doc_assistant_prompt),
                                                         ("human", "The following is the chat history for your reference: {chat_history}")])


def form_doc_upload_assistant(state):
    doc_to_collect = get_next_doc_to_collect(state.docs_to_collect)
    print("\n\n\nAssistant will be collecting the following docs:",doc_to_collect[0])
    chain = form_doc_assistant_prompt_template | llm
    updated_doc_collector_state = copy.deepcopy(state.doc_collector_state)
    updated_doc_collector_state.selected_doc1 = doc_to_collect[0]
    
    print("Updated doc collector state:", updated_doc_collector_state)

    updated_flags = APIFlags(current_conversation_type="upload", stepper="2")

    res = chain.invoke({"doc_to_collect": doc_to_collect[0], 
                        "state":updated_doc_collector_state.doc1_error,
                        "chat_history":trimmed_history(state.history)})


    return{
        "flags": updated_flags,
        "doc_collector_state": updated_doc_collector_state,
       "output":[res]
    }

# Interrupt After
def upload_form_doc(state):
    flags = copy.deepcopy(state.flags)
    flags.current_conversation_type = "upload"
    return{
        "flags":flags
    }



#AZURE DI CODE


# Initialize clients
document_analysis_client = DocumentAnalysisClient(
    endpoint=Constant.DI_API_ENDPOINT, 
    credential=AzureKeyCredential(Constant.DI_KEY)
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
        return f"The user has uploaded {id_document_info.doc_type} type document. Please upload the document again."
    
    return extracted_information

def extract_ssn_info(sas_url:str):
    extracted_information = {}
    confidence = 0
    
    print(f"SAS URL: {sas_url}")
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
        return f"The user has uploaded {id_document_info.doc_type} type document. Information could not be extracted from the document. Please try to upload the document again."
    
    return extracted_information



def extract_info_from_form_doc(state):
    map_dict = {"Passport":extract_passport_info, "SSN":extract_ssn_info}

    extracted_form_doc_info = map_dict[state.doc_collector_state.selected_doc1](state.file_sas_url)

    if type(extracted_form_doc_info) != dict:
        updated_doc_collector_state = copy.deepcopy(state.doc_collector_state)
        updated_doc_collector_state.doc1_verification = False
        updated_doc_collector_state.doc1_error = extracted_form_doc_info

        return{
            "doc_collector_state": updated_doc_collector_state,
            "history":[SystemMessage(content= "An error occoured while trying to process the document. User is advised to re-upload the document.")]
        }

    else:
        updated_doc_collector_state = copy.deepcopy(state.doc_collector_state)
        updated_doc_collector_state.doc1_verification = True
        updated_doc_collector_state.doc1_extracted_info = extracted_form_doc_info
        updated_doc_collector_state.doc1_error = None
        print(f"Uploaded {state.doc_collector_state.selected_doc1} has been successfully processed.")
        
        # LLM output in the document structure
        llm_w_struct = llm.with_structured_output(globals()[state.doc_collector_state.selected_doc1])

        form_res = llm_w_struct.invoke(str("If the information to be filled in the fields is not present, store 'Information not present in the uploaded form'\n\n instead of leaving them None. Make sure to only provide json/dictionary without any spaces\n\n"+pprint.pformat(state.filled_form_extracted_structured_info)))
        
        # Information extracted from the filled form
        updated_doc_collector_state.doc1_information = form_res.__dict__
        print(f"Collected information from the form:\n {pprint.pformat(form_res)}")
        
        return{
            "doc_collector_state": updated_doc_collector_state,
            "history":[SystemMessage(content= f"Uploaded {state.doc_collector_state.selected_doc1} has been successfully processed.")] 
        }


def form_collector_init(state):
    updated_docs_to_collect = copy.deepcopy(state.docs_to_collect)

    for i in updated_docs_to_collect:
        if i['collected'] == False:
            i['collected'] = True
            break
    
    num_docs_to_collect = 0
    for i in updated_docs_to_collect:
        if i['collected'] == False:
            num_docs_to_collect += 1

    if num_docs_to_collect ==0:
        updated_flags = copy.deepcopy(state.flags)
        updated_flags.stepper = "3"
        # updated_flags.current_conversation_type = "review"

        return{
            "flags":updated_flags,
            "history": [SystemMessage(content="All the documents have been collected. Please proceed to review the collected documents.")],
            "output": [SystemMessage(content="All the documents have been collected. Please proceed to review the collected documents.")],
            "docs_to_collect": updated_docs_to_collect,
        }
  
    updated_doc_collector_state = DocCollectorState()
    updated_doc_collector_state.selected_doc1 = get_next_doc_to_collect(updated_docs_to_collect)[0]

    return{
        "docs_to_collect": updated_docs_to_collect,
        "doc_collector_state": updated_doc_collector_state
    }
    