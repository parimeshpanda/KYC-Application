from pydantic import BaseModel, Field
from typing import Optional, Literal

class InitialState(BaseModel):
    kyc_for: Optional[Literal["Individual","Organization", "None"]] = Field(
        description="Whether the KYC is being performed for an individual or an organization.",
        default = None
        )
    
    if_kyc_with_uploaded_document: Optional[bool] = Field(
        description= "Whether the user wants to perform KYC by uploading a Pre-Filled form or not.",
        default= None
    )
    organization_type: Optional[Literal["SoleProprietorship", "PartnershipFirm", "LimitedLiabilityPartnership", "PrivateOrPublicLimitedCompany", "None"]] = Field(
        description="The type of organization for which the KYC is being performed.",
        default = None
        )
    user_confirmation: Optional[bool] = Field(
        description="Whether the user has confirmed the information provided.",
        default = None
        )