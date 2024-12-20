import operator
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Annotated


# class SoleProprietorship(BaseModel):
#     pass

# class LimitedLiabilityPartnership(BaseModel):
#     pass

# class PrivateOrPublicLimitedCompany(BaseModel):
#     pass

#add functions
class BusinessLicense(BaseModel):
    license_number:Optional[str] = Field(description="The License Number provided by the user.", default=None)
    license_issue_date: Optional[str] = Field(description="The Issue Date of the Business License.(Should be stored in YYYY-MM-DD format)[The field is compulsory(do not display to user)]", default=None)
    license_expiry_date: Optional[str] = Field(description="The Expiry Date of the Business License.(Should be stored in YYYY-MM-DD format)[The field is compulsory(do not display to user)]", default=None)
    user_confirmation: Optional[bool] =Field(description="Whether the user has confirmed the information provided.", default=None)

class CertificateofIncorporation(BaseModel):
    issue_date: Optional[str] = Field(description="The Issue Date of the Certificate Of Incorporation.", default=None)
    user_confirmation: Optional[bool] =Field(description="Whether the user has confirmed the information provided.", default=None)

class PrivateOrPublicLimitedCompany(BaseModel):
    
    org_location: Optional[Literal["USA", "India", "EU", "None"]] = Field(
        description= "The location of the organization user wants to do kyc for. Can only be USA, India or EU.",
        default = None
    )

    firm_name: Optional[str] = Field(
        description= "The name of the organization the user provided for KYC.",
        default = None
    )

    # license_number: Optional[str] = Field(
    #     description= "The business license number of the organization , issued by the government.",
    #     default = None
    # )

    # issue_date_of_license: Optional[str] = Field(
    #     description= "The issue date of the business license of the organization. (Should be stored in YYYY-MM-DD format)[The field is compulsory(do not display to user)]",
    #     default=None
    # )

    # expiry_date_of_license: Optional[str] = Field(
    #     description= "The expiry date of the business license of the organization. (Should be stored in YYYY-MM-DD format)[The field is compulsory(do not display to user)]",
    #     default= None
    # )

    num_firm_members: Optional[int] = Field(
        description= "Number of members in the board of the organizationt the user wants to do kyc for. MUST BE MORE THAN 1.",
        default= None
    )

    user_confirmation: Optional[bool] = Field(
        description= "Whether the user is satisfied wit the information they have provided.",
        default = None
    )


class PrivateOrPublicLimitedCompanyMember(BaseModel):
    board_member_name: Optional[str] = Field(
        description= "The Full Name name of the nth board member of the organization.",
        default = None
    )

    board_member_selected_doc: Optional[Literal["Passport","SSN", "None"]] = Field(
        description="The document that the user has the option to provide for the KYC process.",
        default = None
    )

    user_confirmation : Optional[bool] = Field(
        description= "Whether the user has confirmed the information provided.",
        default = False
    )


class PrivateOrPublicLimitedCompanyMemberDoc(BaseModel):
    doc_uploaded: Optional[bool] = Field(description = "Not to be updated by the LLM.", default = None)
    
    # Can be removed?
    board_member_document: Optional[List[dict]] = Field(description = "Not to be updated by the LLM.", default = [{"doc": ["Passport", "SSN", "None"], "collected": False}])
    
    document_information: Optional[dict] = Field(description = "Not to be updated by the LLM.", default = None)

    extracted_document_information: Optional[dict] = Field(description = "Not to be updated by the LLM.", default= None)

class OrgDocCollectorState(BaseModel):
    selected_doc: Optional[Literal["BusinessLicense", "CertificateofIncorporation", "None"]] = Field(
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


class OrganizationState(BaseModel):
    basic_org_info: Optional[BaseModel] = PrivateOrPublicLimitedCompany()
    org_doc_collector_state :Optional[BaseModel] = OrgDocCollectorState()
    org_docs_to_collect : Optional[List[dict]] = [{"doc": ["BusinessLicense", "None"], "collected": False},{"doc":["CertificateofIncorporation", "None"], "collected":False}]
    all_collected_org_docs: Annotated[List[dict], operator.add] = []
    all_board_member_information: Annotated[List[dict], operator.add] = []
    current_member_info: Optional[BaseModel] = PrivateOrPublicLimitedCompanyMember()
    current_member_doc_info: Optional[BaseModel] = PrivateOrPublicLimitedCompanyMemberDoc()
    # allowed_member_docs : Optional[dict] = [{"doc": ["Passport", "SSN", "None"], "collected": False}]
    num_board_members_collected: Optional[int] = 0
    