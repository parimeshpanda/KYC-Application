from typing import Optional, Literal
from pydantic import BaseModel, Field

class PEPInfo(BaseModel):
    pep_extracted_db: Optional[bool] = Field(
        default=None,
        description="If the DB confirms that the user has held a position in a political party or has had political exposure in the past 5 years."
    )
    political_exposure: Optional[bool] = Field(
        description="If the user has held the position in a polictical party or has had political exposure in the past 5 years.", default=None)
    
    bank_acc_no: Optional[str] = Field(
        description="The full bank account number of the user.", default=None)
    
    credit_score: Optional[int] = Field(
        description="The credit score of the user.", default=None)
    
    pep_expected_response: Optional[bool] = Field(
        default=None,
        description="If the User confirms that the user has held a position in a political party or has had political exposure in the past 5 years."
    )

    db_bank_acc_no: Optional[int] = Field(
        description="The full bank account number of the user fetched from the DB to cross check the information of the user.", default=None
    )

    db_credit_score: Optional[int] = Field(
        description="The credit score of the user fetched from the DB to cross check the information of the user.", default=None
    )



class PEPOrgInfo(BaseModel):
    high_risk_factor_db: Optional[bool] = Field(
        default=None,
        description="If the DB confirms that the company has linked with a political party or has had political exposure in the past 5 years."
    )
    annual_revenue: Optional[str] = Field(
        description="Annual revenue of the company", default=None)
    
    pep_members: Optional[Literal["Yes", "No", "None"]] = Field(
        description="Are any of the board members part of political organizaitions?", default=None)
    
    dividends_pq: Optional[str] = Field(
        description="Last quarters dividends released to stakeholders", default=None)