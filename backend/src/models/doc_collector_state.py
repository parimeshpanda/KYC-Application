from pydantic import BaseModel, Field
from typing import Optional, Literal

# Add supported document info here
class Passport(BaseModel):
    passport_number:Optional[str] = Field(description="The Passport Number provided by the user.", default=None)
    passport_issue_date: Optional[str] = Field(description="The Issue Date of the Passport.", default=None)
    passport_expiry_date: Optional[str] = Field(description="The Expiry Date of the Passport.", default=None)
    place_of_birth: Optional[str] = Field(description="The Place of Birth of the user.", default=None)
    user_confirmation: Optional[bool] =Field(description="Whether the user has confirmed the information provided.", default=None)


class SSN(BaseModel):
    ssn_number:Optional[str] = Field(description="The SSN Number provided by the user.", default=None)
    user_confirmation: Optional[bool] =Field(description="Whether the user has confirmed the information provided.", default=None)


# class Adhaar(BaseModel):
#     adhaar_number:Optional[str] = Field(description="The Adhaar Number provided by the user.")
#     user_confirmation: Optional[bool] =Field(description="Whether the user has confirmed the information provided.")

# class PAN(BaseModel):
#     pan_number:Optional[str] = Field(description="The PAN Number provided by the user.")
#     father_name: Optional[str] = Field(description="The Father's Name of the user.")
#     dob: Optional[str] = Field(description="Date of Birth of the user.")
#     user_confirmation: Optional[bool] =Field(description="Whether the user has confirmed the information provided.")



class DocCollectorState(BaseModel):
    selected_doc1: Optional[Literal["Passport", "SSN", "None"]] = Field(
        description="The Document that the user chooses to provide for the KYC verification.", default=None
    )

    if_doc1_uploaded: Optional[bool] = Field(
        description="If user has uploaded the file.", default=None
    )

    doc1_information: Optional[dict]= Field(
        description="LLM SHOULD NOT UPDATE THIS FIELD. The field contains info about the uploaded document, provided by the user.", default={}
    )

    doc1_verification: Optional[bool]= Field(
        description="LLM SHOULD NOT UPDATE THIS FIELD. If the doc was successfully processed by DI.", default=None
    )

    doc1_error: Optional[str] = Field(
        description= "LLM SHOULD NOT UPDATE THIS FIELD. If there was an error in processing the document.", default=None
    )

    doc1_extracted_info: Optional[dict] = Field(
        description="LLM SHOULD NOT UPDATE THIS FIELD. Information extracted by DI from the uploaded DOC.", default=None
    )