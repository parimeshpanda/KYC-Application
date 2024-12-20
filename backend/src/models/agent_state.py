import operator
from typing import Sequence, Annotated, Optional, List, TypedDict, Union, Literal

# from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field

from src.models.init_state import InitialState
from src.models.organization_state import OrganizationState
from src.models.required_information import RequiredInformation
from src.models.retriever_state import RetrieverState
from src.models.doc_collector_state import DocCollectorState
from src.models.organization_state import OrgDocCollectorState,BusinessLicense, CertificateofIncorporation, PrivateOrPublicLimitedCompany, PrivateOrPublicLimitedCompanyMember, PrivateOrPublicLimitedCompanyMemberDoc
from src.models.pep_state import PEPInfo, PEPOrgInfo


class APIFlags(BaseModel):
    current_conversation_type: Literal["conversation", "upload", "update", "review", "Pass", "Fail"] = "conversation"
    stepper: str = "0"
    # 0 = Demographic info collection
    # 1 = customer info collection
    # 2 = Proof of info collection
    # 3 = Comparator 
    
    # 3 = Financial info collection (To be added after PEP nodes are completed)

class ComparatorState(BaseModel):
    kyc_result : Optional[Literal["Pass","Fail"]] = Field(
        description="Result of the KYC. Pass or Fail", 
        default=None)
    
    result_explanation : Optional[str] = Field(
        description="DETAILED explanation of the result of the KYC. Mention COMPLETE thought process and each step taken inorder to get the answer!! Mention each decision and why that decision was taken along with which tools were called in order to reach that decision. This must be as detailed as possible!(Preferrably in points.)", 
        default=None)
    
    kyc_for : Optional[str] = Field(
        description= "The name of the person for whom the KYC is being done. THIS FIELD IS NOT TO BE MODIFIED BY THE LLM.", 
        default=None)
    
    kyc_type: Optional[Literal["Individual","Organization", "None"]] = Field(
        description="Whether the KYC is being performed for an individual or an organization. THIS FIELD IS NOT TO BE MODIFIED BY THE LLM.",
        default = None
        )
    # verbose_result = Optional[str] = Field(description = "Verbose explanation of the result of the KYC", default=None)


class UnifiedUserInformation(BaseModel):
    user_country : Optional[Literal["EU","USA", "India", 'None']]= Field(
        description="The Country Entered by the user.", 
        default=None)
    
    user_first_name : Optional[str] = Field(
        description="The Full Name provided by the user.", 
        default=None)
    
    user_last_name : Optional[str] = Field(
        description="The Last Name provided by the user.", 
        default=None)
    
    user_father_name : Optional[str] = Field(
        description="The Father's Name provided by the user.", 
        default=None)
    
    user_gender: Optional[Literal["Male", "Female", "Other", "None"]]= Field(
        description = "The Gender provided by the user. Can only be Male, Female or Other.", 
        default=None)
    
    user_marital_status : Optional[Literal["Single", "Married", "Divorced", "Widowed", "None"]]= Field(
        description="The Marital Status provided by the user.", 
        default=None)

    user_date_of_birth: Optional[str]= Field(
        description="The Date of Birth provided by the user.", 
        default=None)
    
    user_passport_number: Optional[str]= Field(
        description="Passport Number provided by the user.", 
        default=None)
    
    user_passport_issue_date: Optional[str]= Field(
        description="Passport Issue Date provided by the user.", 
        default=None)
    
    user_passport_expiry_date: Optional[str]= Field(
        description="Passport Expiry Date provided by the user.", 
        default=None)
    
    user_ssn_number: Optional[str]= Field(
        description="SSN Number provided by the user.", 
        default=None)
    
    user_confirmation : Optional[bool]= Field(
        description="Whether the user has confirmed the infromation they have provided.",
        default= False)
    
    user_place_of_birth: Optional[str] = Field(
        description= "The place of birth/address of the user.",
        default=None)


class AgentState(BaseModel):
    user_input: Optional[str] = None
    flags: Optional[BaseModel] = APIFlags(current_conversation_type="conversation", stepper="0")
    file_sas_url: Optional[str] = None  
    kyc_verifier_state: Optional[ComparatorState] = ComparatorState()

    initial_state: InitialState = InitialState()
    user_information : RequiredInformation = RequiredInformation()
    retriever_state: RetrieverState = RetrieverState()  # Not being used currently
    history : Annotated[Sequence[BaseMessage],operator.add]
    output : Annotated[List[BaseMessage],operator.add]
    doc_collector_state: Optional[Union[BaseModel, dict]] = None
    doc_info_history: Annotated[List[BaseMessage], operator.add]
    docs_to_collect: Optional[List[dict]] = [{"doc": ["Passport", "SSN", "None"], "collected":False}]# Using Fixed documents for now (Only for USA)
    all_collected_docs: Annotated[List[dict], operator.add]
    
    # Organization State
    # organization_state: Optional[BaseModel] = OrganizationState()   
    basic_org_info: Optional[BaseModel] = PrivateOrPublicLimitedCompany()
    org_doc_collector_state :Optional[BaseModel] = OrgDocCollectorState()
    org_docs_to_collect : Optional[List[dict]] = [{"doc": ["BusinessLicense", "None"], "collected": False},{"doc":["CertificateofIncorporation", "None"], "collected":False}]
    all_collected_org_docs: Annotated[List[dict], operator.add] = []
    all_board_member_information: Annotated[List[dict], operator.add] = []
    current_member_info: Optional[BaseModel] = PrivateOrPublicLimitedCompanyMember()
    current_member_doc_info: Optional[BaseModel] = PrivateOrPublicLimitedCompanyMemberDoc()
    # allowed_member_docs : Optional[dict] = [{"doc": ["Passport", "SSN", "None"], "collected": False}]
    num_board_members_collected: Optional[int] = 0


    pep_information: Optional[PEPInfo] = PEPInfo()
    org_pep_information: Optional[PEPOrgInfo] = PEPOrgInfo()


    filled_form_extracted_info: Optional[str] = None
    filled_form_extracted_structured_info: Optional[BaseModel] = UnifiedUserInformation()
    all_form_extracted_doc_info: List = []
    all_form_collected_doc_info: Annotated[List[dict], operator.add] = [{}]
