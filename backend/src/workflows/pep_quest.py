import copy
from dotenv import load_dotenv
from src.util.llm_singleton import LLMSingleton
from langchain_core.prompts import ChatPromptTemplate
from src.util.utils import trimmed_history 
from src.models.agent_state import AgentState
from src.models.pep_state import PEPInfo
from src.models.model import PEPData
from src.config.db_config import POSTGRES_CONFIG, db_connection, get_db_session
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean

load_dotenv()

llm = LLMSingleton().get_llm()

pep_assistant_prompt = """**Task**
You are a helpful assistant that helps with the KYC verification of users. Your job is to collect and validate sensitive financial and political exposure information.

**Information that needs to be collected from the user**
*political_exposure: Required response must be a boolean true or false. (Is the user currently holding, or in the past 5 years held, any public or political position in the country. Do not display or accept "None" as an option)
*bank_acc_no: Must be exactly 10 digits, numbers only. (User must enter their bank account number. Do not display or accept "None" as an option)
*credit_score: Must be 3 digits between 300-850. (User must enter their credit score. Do not display or accept "None" as an option)

**Rules**
While collecting the information make sure to follow the following rules:
* "None" is not an acceptable response for any of the fields if the value of any fields is "None" then you must ask the user to provide the information again.
* Do not show "None" as the option when you are asking for any question.
* Collection of ALL information listed above is mandatory - no exceptions.
* Each field must be collected in the exact order listed above.
* Collect only one piece of information at a time and validate before proceeding.
* For information updates, always check the current state before confirming or denying the update.
* Provide clear explanations when rejecting invalid input formats or values.
* Users cannot skip fields or proceed without completing previous information.
* DO NOT FILL IN THE INFORMATION, YOU MUST COLLECT IT FROM THE USER.

To track the state of all the steps you will be provided with the current state of the process:
{state}
"""

pep_system_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* The value of political_exposure feild must be a boolean input true or false if the user enters anything else set the value to 'None' .
* For the bank_acc_no feild, if the user enters any other information than the mentioned ones, set the field value to 'None'.
* Whenever the user wants to UPDATE or MAKE A CORRECTION to a field, ONLY THEN change that field to 'None'.
* If the user has entered all the information required, DO NOT ASK TO UPDATE OR if he would like to change something!
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""

pep_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",pep_assistant_prompt),
        (
            "human",
            "Chat History: {chat_history}"
            "Already Collected Information: {state}"
        )
    ]
)


pep_collection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",pep_system_prompt),
        (
            "human",
            "Chat History: {chat_history}"
            "Already Collected Information: {collected_information}" #?
            "user_input: {user_input}" #?
        )
    ]
)


def pep_assistant_node(state: AgentState):
    pep_assistant_chain = pep_assistant_prompt | llm 

    res = pep_assistant_chain.invoke(
        {
            "chat_history": trimmed_history(state.history),
            "collected_information": state.pep_information,
            "state": state
        }
    )
    return {
        "history":[res],
        "output": [res]
    }


def combine_required_inf_new(old_info: PEPInfo, new_info: PEPInfo):

    old_info_dict = old_info.__dict__
    new_info_dict = new_info.__dict__
    old_info_dict.update({k:new_info_dict[k] for k in new_info_dict if new_info_dict[k] is not None}) #updates non none values

    new_info_obj = PEPInfo(**old_info_dict)
    
    return new_info_obj


def pep_collect_information(state: AgentState):

    structured_output_llm  = llm.with_structured_output(PEPInfo)
    information_chain = pep_collection_prompt | structured_output_llm

    information_stdin = state.user_input
    res = information_chain.invoke(
        {
            "chat_history": trimmed_history(state.output),
            "user_input": information_stdin,
            "collected_information": state.pep_information
        }
    )
    res = combine_required_inf_new(state.pep_information, res)
    # updated_res= PEPInfo(res)

    return {
        "pep_information":res,
        "history": [HumanMessage(content=information_stdin)],
        "output": [HumanMessage(content=information_stdin)]
    }


def get_from_pep_info(config: dict, doc_type, document_no: int, state: AgentState) -> bool:
    """
    Retrieve PEP information from database
    Returns True if person is politically exposed, False otherwise
    """
    try:
        engine = db_connection(config)
        if engine is None:
            print("engine not found")
            return False
        if doc_type == 'ssn':
            with get_db_session(engine) as session:
                info = session.query(PEPData.politically_exposed,
                                     PEPData.pep_user_input,
                                     PEPData.bank_acc_no,
                                     PEPData.credit_score
                                     )\
                            .filter_by(ssn_no=document_no)\
                            .first()                
                if info is None:
                    print("no SSN information found")
                    return False
                
                is_pep = bool(info.politically_exposed)
                
        elif doc_type == 'passport':
            with get_db_session(engine) as session:
                info = session.query(PEPData.politically_exposed,
                                     PEPData.pep_user_input,
                                     PEPData.bank_acc_no,
                                     PEPData.credit_score
                                     )\
                            .filter_by(passport_no=document_no)\
                            .first()

                if info is None:
                    print("no passport information found")
                    return False
                
                is_pep = bool(info.politically_exposed)  
        state.pep_information.pep_expected_response = bool(info.pep_user_input)
        state.pep_information.db_bank_acc_no = info.bank_acc_no
        state.pep_information.db_credit_score = info.credit_score  
        return is_pep
    
    finally:
        if engine:
            engine.dispose()



def extract_pep_info(state: AgentState):
    """Checks PEP status"""
    if (state.initial_state.if_kyc_with_uploaded_document== False) :
        doc_type= str(state.all_collected_docs[0]['selected_doc1']).lower()
        print("document type:", doc_type)
        if(doc_type== 'ssn'):
            doc_number=int(state.all_collected_docs[0]['doc1_information']['ssn_number'])
        elif(doc_type== 'passport'):
            doc_number=str(state.all_collected_docs[0]['doc1_information']['passport_number']).upper()
        else:
            print('Invalid document type')
    
    elif(state.initial_state.if_kyc_with_uploaded_document== True):
        doc_type= state.doc_collector_state.selected_doc1.lower()
        print("document type:", doc_type)
        if(doc_type== 'ssn'):
            doc_number=int(state.doc_collector_state.doc1_information['ssn_number']) #! int(state.doc_collector_state.doc1_extracted_info['DocumentNumber'].replace('-', '')) use this when LLM imformation is being extracted .replace('-', '')
        elif(doc_type== 'passport'):
            doc_number= state.doc_collector_state.doc1_information['passport_number'].upper() # ! state.doc_collector_state.doc1_extracted_info['DocumentNumber']
        else:
            print('Invalid document type')

    result = get_from_pep_info(POSTGRES_CONFIG, doc_type, doc_number,state)
    print(result)
    # state.pep_information.pep_extracted_db= result
    updated_pep_state = copy.deepcopy(state.pep_information)
    updated_pep_state.pep_extracted_db = result
        
    # res=state.pep_information.dict()

    return {
        "pep_information": updated_pep_state,
        "messages": [
            {
                "role": "system",
                "content": f"PEP check completed for document number: {doc_number}"
            }
        ]
    }