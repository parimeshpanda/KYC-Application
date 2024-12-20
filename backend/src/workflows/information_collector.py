from typing import List
import copy
import tiktoken

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI

from src.models.agent_state import AgentState
from src.models.required_information import RequiredInformation
from src.util.llm_singleton import LLMSingleton
from src.util.utils import trimmed_history

assistant_system_prompt = """ **Task** 
You are a helpful assistant that performs KYC of users. Your Job is to collect information from the user. The following information needs to be collected from the user.

** Information to be collected from user**
* user_country : The country that the user resides in. (Can only be "europian union", "usa", or "india") (If the user enters some other country ask them to enter again as the country is not valid.)
* user_first_name : The First Name provided by the user.
* user_last_name : The Last Name provided by the user.
* user_father_name : The Father's Full Name provided by the user.
* user_gender : The gender provided by the user. Can only be "Male", "Female", "Other".
* user_marital_status : The Marital Status provided by the user. Can only be "Single", "Married", "Divorced", "Widowed".
* date_of_birth : The Date of Birth provided by the user. (User can provide the date in any format information inside this paranthese should not be displayed to the user.)
* user_confirmation: The confirmation from the user that the information provided by them is correct. (Can only be True or False)

While collected the information the following points need to be adhered to strictly.
* You must greet the user only once, at the start of the conversation.
* It is compulsory for you to collect all the information mentioned above. Do not try to skip collecting ANY information.
* DO NOT TRY TO REASON WITH WHAT INFORMATION IS TO BE COLLECTED, COLLECT THE AFOREMENTIONED INFORMATION AS IT IS.
* All the information must be collected sequentailly and one field at a time. 
* Under no circumstances can the user proceed without providing the previous information.
* All the user infromation will be handled securely and with utmost care.
* If the user enters wrong information, you should explain why their input is wrong.
* To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to confirm the priovided information. 
* You should collect all the necessary information and none of the field should be "None".
* If the user asks to update the field, OTHER FIELDS SHOULD HAVE THE PREVIOUSLY ENTERED VALUE, THEY MUST NOT BE COLLECTED AGAIN.
* DO NOT FILL IN THE INFORMATION, YOU MUST COLLECT IT FROM THE USER.
* Whenever user updates information, ask for the confirmation of all details again. IT IS VITAL THAT THE INFORMATION RETRIEVED IS CORRECT.
* To ask the next question, you must look at "Already Collected information:" below, and ask the next question accordingly.
"""

information_system_prompt = """
* You are an information collection agent. Your job is to look at the given input and update the fields.
* The country given by user should not be case sensitive so be it "USA" or "usa" treat them as one.
* If the user enters countries other than usa, eu, india, fill in the field as None.
* You should be smart enough to understand if the user enters "I live in the USA" or "I am from the USA" or something similar, you should be able to extract the country name.
* For the user_gender field and user_marital_status field, if the user enters any other information than the mentioned ones, set the field value to None.
* Only update the field that has been askes from the user not any othe fields.
* Whenever the user wants to UPDATE or MAKE A CORRECTION to a field, ONLY THEN change that field to None.
* To update the to user_confirmation field, the user will be dispayed all information they have entered, if the user says "yes" to the confirm the information, UPDATE THE FIELD TO True.
* The date_of_birth field should be stored in the format "YYYY/MM/DD". If the user enters any other format, then you must convert it into YYYY/MM/DD format.
* While storing information, make sure that the boolean values are lower case (For example, True should be stored as true) and the None values are stored as null. This is to maintain a valid JSON object.
"""
#* The date of birth field should be in the format "YYYY-MM-DD". If the user enters any other format, then you must save the date in the correct format.
# * To update the user_country_updation field, whenever the user asks to update the country, change the field to True.

llm = LLMSingleton().get_llm()

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",assistant_system_prompt),
        (
            "human",
            "Chat History: {chat_history}"
            "Already Collected Information: {collected_information}"
        )
    ]
)

information_collection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", information_system_prompt),
        (
            "human",
            "Chat History: {chat_history}"
            "User Input: {user_input}"
            "Information Collected So Far: {collected_information}"
        )
    ]
)

def assistant_node(state: AgentState):

    assistant_chain = assistant_prompt | llm 

    
    res = assistant_chain.invoke(
        {
            "chat_history": trimmed_history(state.history),
            "collected_information": state.user_information
        }
    )
    return {
        "history":[res],
        "output": [res]
    }

# collect_info_system_prompt = """You are a helpful assistant that is tasked with collecting information for the kyc of the user.
# **The following information is to be collected by the user**
# * user_country : The country that the user resides in. (Make sure that the name does not contain any numerical characters.)
# * user_name : The full name of the user.
# * user_ssn : The Social Security Number of the user.
# * user_passport_no : The Passport number of the user.
# * user_confirmation : Whether the collected information has been validated by the user.
# """

# def combine_required_info(info_list: List[RequiredInformation]) -> RequiredInformation:
#     info_list = [info for info in info_list if info is not None]

#     if len(info_list) == 1:
#         return info_list[0]
#     combined_info = {}
#     for info in info_list:
#         for key, value in info.dict().items():
#             if value is not None:
#                 combined_info[key] = value
#     return RequiredInformation(**combined_info)

def combine_required_inf_new(old_info: RequiredInformation, new_info: RequiredInformation):
    # combined_info = {}
    # for key, value in new_info.__dict__.items():
    #     if value is not None:
    #         combined_info[key] = value

    old_info_dict = old_info.__dict__
    new_info_dict = new_info.__dict__
    old_info_dict.update({k:new_info_dict[k] for k in new_info_dict if new_info_dict[k] is not None})

    new_info_obj = RequiredInformation(**old_info_dict)
    
    return new_info_obj
    


def collect_information(state: AgentState):
    encoding = tiktoken.encoding_for_model("gpt-4-turbo")

    print("USER INFORMATION: ",state.user_information)
    structured_output_llm  = llm.with_structured_output(RequiredInformation)
    information_chain = information_collection_prompt | structured_output_llm

    information_stdin = state.user_input

    res = information_chain.invoke(
        
        {
            "chat_history": trimmed_history(state.history),
            "user_input": information_stdin,
            "collected_information": state.user_information
        }
    )
    print("RES COLLECT INFO: ",res)   

    res = combine_required_inf_new(state.user_information, res)
    
    if res.user_confirmation == True:
        updated_flag = copy.deepcopy(state.flags)
        updated_flag.stepper = '2'

        return {
        "flags": updated_flag,
        "user_information":res,
        "history": [HumanMessage(content=information_stdin)],
        "output": [HumanMessage(content=information_stdin)]
    }

    return {
        "user_information":res,
        "history": [HumanMessage(content=information_stdin)],
        "output": [HumanMessage(content=information_stdin)]
    }

