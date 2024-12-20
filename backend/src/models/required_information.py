from typing import Optional, Literal, Union

# from langgraph.graph import add_messages
from pydantic import BaseModel,Field


class RequiredInformation(BaseModel):
    # user_country : Union[Literal["EU"], Literal[ "USA"], Literal["INDIA"], Literal[None]] = Field(
    #     description="The Country Entered by the user.")

    user_country : Optional[Literal["EU","USA", "India", 'None']]= Field(
        description="The Country Entered by the user.", default=None)
    
    user_first_name : Optional[str] = Field(
        description="The Full Name provided by the user.", default=None)
    
    user_last_name : Optional[str] = Field(
        description="The Last Name provided by the user.", default=None)
    
    user_father_name : Optional[str] = Field(
        description="The Father's Name provided by the user.", default=None)
    
    user_gender: Optional[Literal["Male", "Female", "Other", "None"]]= Field(
        description = "The Gender provided by the user. Can only be Male, Female or Other.", default=None)
    
    user_marital_status : Optional[Literal["Single", "Married", "Divorced", "Widowed", "None"]]= Field(
        description="The Marital Status provided by the user.", default=None)

    user_date_of_birth: Optional[str]= Field(
        description="The Date of Birth provided by the user.", default=None)
    # user_ssn : Optional[str]=Field(
    #     description= "The Social Security Number provided by the user.", default=None)
    
    # user_passport_no : Optional[str]= Field(
    #     description="The passport number provided by the user.", default=None)
    
    user_confirmation : Optional[bool]= Field(
        description="Whether the user has confirmed the infromation they have provided.",
        default= False)
    
    user_country_updation : Optional[bool] = Field(
        description="Whether the user has asked for their country to be updated/changed.", 
        default=False)