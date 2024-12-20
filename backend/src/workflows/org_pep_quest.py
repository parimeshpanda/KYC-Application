from dotenv import load_dotenv
from src.util.llm_singleton import LLMSingleton
from langchain_core.prompts import ChatPromptTemplate
from src.util.utils import trimmed_history #, combine_required_info
from src.models.agent_state import AgentState
from src.models.pep_state import PEPOrgInfo
from src.models.model import TableData
from src.config.db_config import POSTGRES_CONFIG
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from datetime import datetime

llm = LLMSingleton().get_llm()


org_pep_assistant_prompt = """**Task**
You are a helpful assistant that helps with the KYC verification of users. Your job is to collect and validate sensitive financial and political exposure information.

**Information that needs to be collected from the user**
*annual_revenue: Annual revenue of the company. (Do not display or accept "None" as an option)
*pep_members: Are any of the board members part of political organizations. (Is any employee of the company currently holding, or in the past 5 years held, any public or political position in the country. User must enter Yes/No. Do not display or accept "None" as an option)
*dividends_pq: What were the last quarters dividends released to the stakeholders. (User must enter their company's las quarter dividends. Do not display or accept "None" as an option)

**Rules**
While collecting the information make sure to follow the following rules:
* "None" is not an acceptable response for any of the fields if the value of any fields is "None" then you must ask the user to provide the information again.
* Do not show "None" as the option when you are asking for any question.
* Collection of ALL information listed above is mandatory - no exceptions.
* DON'T collect ANY information other than the above mentioned information. 
* Each field must be collected in the exact order listed above.
* Collect only one piece of information at a time and validate before proceeding.
* For information updates, always check the current state before confirming or denying the update.
* Provide clear explanations when rejecting invalid input formats or values.
* Users cannot skip fields or proceed without completing previous information.
* DO NOT FILL IN THE INFORMATION, YOU MUST COLLECT IT FROM THE USER.
* Do not ask the user for any assistance on information that is not required!

To track the state of all the steps you will be provided with the current state of the process:
{state}
"""

org_pep_system_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* The value of annual_revenue feild must cleary mention the amount of money the company generates anually, if the user enters anything else set the value to 'None' .
* The value of pep_members feild must cleary mention  as "Yes" or "No" if any of the members of the organisation are politically exposed, if the user enters anything else set the value to 'None' .
* The value of dividends_pq feild must cleary mention last quarters dividends the company has release to the stakeholders, if the user enters anything else set the value to 'None' .
* DO NOT ASK FOR ANY INFORMATION EXCEPT FROM THE ABOVE MENTIONED FIELDS.
* Whenever the user wants to UPDATE or MAKE A CORRECTION to a field, ONLY THEN change that field to 'None'.
* If the user has entered all the information required, DO NOT ASK TO UPDATE OR if he would like to change something!
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""


org_pep_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",org_pep_assistant_prompt),
        (
            "human",
            "Chat History: {chat_history}"
            "Already Collected Information: {state}"
        )
    ]
)


org_pep_collection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",org_pep_system_prompt),
        (
            "human",
            "Chat History: {chat_history}"
            "Already Collected Information: {collected_information}"
            "user_input: {user_input}"
        )
    ]
)


def org_pep_assistant_node(state: AgentState):
    pep_assistant_chain = org_pep_assistant_prompt | llm 

    res = pep_assistant_chain.invoke(
        {
            "chat_history": trimmed_history(state.history),
            "collected_information": state.org_pep_information,
            "state": state #?
        }
    )
    return {
        "history":[res],
        "output": [res]
    }


def combine_required_inf_new(old_info: PEPOrgInfo, new_info: PEPOrgInfo):

    old_info_dict = old_info.__dict__
    new_info_dict = new_info.__dict__
    old_info_dict.update({k:new_info_dict[k] for k in new_info_dict if new_info_dict[k] is not None}) #updates non none values

    new_info_obj = PEPOrgInfo(**old_info_dict)
    
    return new_info_obj


def org_pep_collect_information(state: AgentState):

    structured_output_llm  = llm.with_structured_output(PEPOrgInfo)
    information_chain = org_pep_collection_prompt | structured_output_llm

    information_stdin = state.user_input
    res = information_chain.invoke(
        {
            "chat_history": trimmed_history(state.output),
            "user_input": information_stdin,
            "collected_information": state.org_pep_information
        }
    )
    res = combine_required_inf_new(state.org_pep_information, res)
    return {
        "org_pep_information":res,
        "history": [HumanMessage(content=information_stdin)],
        "output": [HumanMessage(content=information_stdin)]
    }


def db_connection(config: dict):
    """Create and return database engine with connection pooling"""
    try:
        conn_string = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
        engine = create_engine(
            conn_string,
            poolclass=QueuePool,
            pool_size=3, 
            max_overflow=5,  
            pool_timeout=30,
            pool_pre_ping=True,
            pool_recycle=1800  
        )
        return engine
    except Exception as e:
        return None
    
@contextmanager
def get_db_session(engine) -> Session:
    """Context manager for database sessions"""
    if engine is None:
        raise ConnectionError("Database engine is not initialized")
        
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def get_org_pep_info(config: dict, business_license_no) -> bool:
    """
    Retrieve PEP information from database
    """
    try:
        engine = db_connection(config)
        if engine is None:
            return False

        with get_db_session(engine) as session:
            info = session.query(TableData.high_risk_factor)\
                         .filter_by(business_license_no=business_license_no)\
                         .first()

            if info is None:
                return False
            
            is_pep = bool(info.high_risk_factor)
            return is_pep
    finally:
        if engine:
            engine.dispose()

def extract_org_pep_info(state: AgentState):
    """Checks Financial Risk status of the company"""

    business_license_no = int(state.organization_state.all_collected_org_docs[0]['Org-BusinessLicense'].doc_information['license_number'])
    print("business_license_no:", business_license_no)

    result = get_org_pep_info(POSTGRES_CONFIG, business_license_no)
    
    state.org_pep_information.high_risk_factor_db = result
    
    res=state.org_pep_information.dict()
    
    return {
        "org_pep_information": state.org_pep_information,
        "messages": [
            {
                "role": "system",
                "content": f"Financial risk check completed for document number: {business_license_no}"
            }
        ]
    }