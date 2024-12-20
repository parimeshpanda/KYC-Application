import os
import json

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain.tools.base import StructuredTool
from langchain_openai import AzureChatOpenAI
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage, AIMessage

from src.util.llm_singleton import LLMSingleton
from src.models.agent_state import ComparatorState
from src.config.db_config import POSTGRES_CONFIG, db_connection, get_db_session
# from src.models.model import PEP_information
PERSONAL_INFO_PATH = "personal_info.json"
DOC_INFO_PATH = "doc_info.json"
USA_GUIDELINES_NAME= "usa_guidelines.txt"
EUROPE_GUIDELINES_NAME= "europe_guidelines.txt"


class KYCVerifier:
    def __init__(self, user_personal_information, user_document_information,politico_informatio):
        self.user_personal_information = user_personal_information
        self.user_document_information = user_document_information
        self.politico_informatio1= politico_informatio
        self.tools = [
            StructuredTool.from_function(self.europe_guidelines),
            StructuredTool.from_function(self.usa_guidelines),
            StructuredTool.from_function(self.personal_information),
            StructuredTool.from_function(self.doc_information),
            StructuredTool.from_function(self.political_information)
        ]
        self.sys_prompt = self._create_system_prompt()
        self.prompt = self._create_prompt()
        # self.llm = self._define_llm()
        self.llm = LLMSingleton().get_llm()
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    @staticmethod
    def usa_guidelines(query: str) -> str:
        """Provide KYC requirements for Individual users in the USA."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..','guidelines', USA_GUIDELINES_NAME)
        with open(file_path, 'r') as file:
            guidelines = str(file.read())
        return guidelines

 
    @staticmethod
    def europe_guidelines(query: str) -> str:
        """Provide KYC requirements for Individual users in Europe."""
        file_path = 'europe_guidelines.txt'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..','guidelines', EUROPE_GUIDELINES_NAME)
        with open(file_path, 'r') as file:
            guidelines = str(file.read())
        return guidelines
    
    def personal_information(self, query: str) -> str:
        """Retrieve all the information provided by the user for comparison with the guidelines."""
        return f"The end user has provided the following KYC requirements for Individual user: {self.user_personal_information}"

    def doc_information(self, query: str) -> str:
        """Returns all the information fetched from the documents."""
        return f"The Information extracted from the documents uploaded by the user: {self.user_document_information}"
    
    def political_information(self, query: str) -> str:
        """
        Returns all the politically exposed information fetched from the database.
        
        Args:
            query (str): Input query (required by StructuredTool)
        
        Returns:
            str: Formatted political information
        """
        return f"The Information extracted from the database for politically exposed user: {self.politico_informatio1}"
    # def political_information(self, query: str) -> str:
    #     """Returns all the information for politically exposed users fetched from the database."""
    #     return f"The Information extracted from the database for politically exposed user: {self.politico_informatio1}"

    @staticmethod
    def _create_system_prompt() -> str:
        return """FIRSTLY the document information provided by "doc_information" tool should have the same information in the matching fields of the personal information fetched with the "personal_information" tool and the information must be SAME. 
        For example, if the personal information tool has the following information:
        [
          {
            "First name": "Shiva",
            "Last Name": "Sharma",
            "Father's Name": "Anish Sharma",
            "Gender": "Male",
            "SSN": "123456789",
            "Marital Status": "Single",
            "Date of Birth": "01/01/1990",
            "Place of Birth": "New York"
          }
        ]
        and the document information tool has the following information:
        [
          {
            "Document Type":"SSN",
            "First name": "Shiva",
            "Last Name": "Sharma",
            "SSN": "123456789"
          }
        ]
        This type of information MUST return true as all the fields that are common are matching exactly in the document information.
        It SHOULD NOT be rejected saying that there is insufficient information. The information provided by the document information tool should be validated with the information present in the personal information tool.
        STRICTLY MATCH each and every document number, date of issue and date of expiry as they must be EXACTLY same while matching the information received from personal information tool and document information tool. Only match the values present in the key-value pairs and no the exact name of the keys. Especially when it comes to documents like Passport. If you fail to catch mismatch in CRITICAL INFORMATION like passport number, Passport Issue date and Passport Expiry date , YOU WILL BE TERMINATED!
        When it compares to matching information like gender: "Male" and "M" are the same response and MUST not be rejected.
        IF they don't match, terminate.
        IF the information provided by personal information tool contains that the Political Exposure is true, ONLY then invoke the "political_information" tool and compare the information provided by the political information tool with the information provided by the political info provide by the personal information tool.
        SECONDLY The document information tool might have lesser information, but the key value pairs of the information provided should EXACTLY match with the info received from personal information tool. NO need to look for details that are not present in the document information. JUST validate the information that is present.
        Based on the country fetched by the information tool call the respective country guidelines tool.
        The document information tool might have lesser information, but the key value pairs of the information should EXACTLY match with the info received from personal information tool.
        For example, if the country fetched by the information tool is USA, then call the tool "usa_guidelines" 
        or if the country fetched by the information tool is Europe, then call the tool "europe_guidelines".
        FINALLY Then use the guidelines as a checklist and compare the information entered by the information tool and check if the information is sufficient and in compliance with the guidelines.
        """

    def _create_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate(
            messages=[
                SystemMessage(content=self.sys_prompt),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ],
            input_variables=['agent_scratchpad', 'input']
        )

    def _create_agent(self) -> AgentExecutor:
        return create_openai_functions_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)

    def run(self):
        result = self.agent_executor.invoke({
            "input": """Print the answer as YES or NO if the KYC guidelines have been satisfied and the KYC is successful or not, based on the validation done. The validation must be proceeded STRICTLY ehrn it comes to comparing document information with user information.
            If "NO" then provide the reason for failure. Check if the information provided has been validated and is in compliance with the regulatory guidelines."""
        })
        return(result['output'])


def compare_info(state):
    personal_info = state.doc_collector_state.doc1_information
    personal_info["First Name"] = state.user_information.user_first_name
    personal_info["Last Name"] = state.user_information.user_last_name
    personal_info["Date of Birth"] = state.user_information.user_date_of_birth
    personal_info["Fathers Name"] = state.user_information.user_father_name
    personal_info["Gender"] = state.user_information.user_gender
    personal_info["Marital Status"] = state.user_information.user_marital_status
    personal_info["User Country"] = state.user_information.user_country

    if state.pep_information.pep_extracted_db == True:
        personal_info["Political Exposure"]= state.pep_information.pep_extracted_db
        personal_info["Political person Input"]= state.pep_information.political_exposure
        personal_info["Bank Account Number"]= state.pep_information.bank_acc_no
        personal_info["Credit Score"]= state.pep_information.credit_score

    collected_doc_info = state.doc_collector_state.doc1_extracted_info
    if(state.doc_collector_state.doc1_extracted_info['DocumentType'] == 'idDocument.usSocialSecurityCard'):
        collected_doc_info['DocumentType'] = 'Social Security Card'
        collected_doc_info['FirstName'] = state.doc_collector_state.doc1_extracted_info['FirstName']
        collected_doc_info['LastName'] = state.doc_collector_state.doc1_extracted_info['LastName']
        collected_doc_info['DocumentNumber'] = state.doc_collector_state.doc1_extracted_info['DocumentNumber'].replace("-", "")

    elif(state.doc_collector_state.doc1_extracted_info['DocumentType'] == 'idDocument.passport'):
        collected_doc_info['DocumentType'] = 'Passport'
        collected_doc_info['FirstName'] = state.doc_collector_state.doc1_extracted_info['FirstName']
        collected_doc_info['LastName'] = state.doc_collector_state.doc1_extracted_info['LastName']
        collected_doc_info['DocumentNumber'] = state.doc_collector_state.doc1_extracted_info['DocumentNumber']
        collected_doc_info['DateOfBirth'] = state.doc_collector_state.doc1_extracted_info['DateOfBirth']
        collected_doc_info['DateOfIssue']= state.doc_collector_state.doc1_extracted_info['DateOfIssue']
        collected_doc_info['DateOfExpiration']= state.doc_collector_state.doc1_extracted_info['DateOfExpiration']
        collected_doc_info['PlaceOfBirth']= state.doc_collector_state.doc1_extracted_info['PlaceOfBirth']
    
    # if state.pep_information.pep_extracted_db == True:

    #     collected_doc_info['PoliticalExposure'] = state.pep_information.pep_extracted_db
    #     collected_doc_info['PoliticalPersonInput'] = state.pep_information.political_exposure
    #     collected_doc_info['BankAccountNumber'] = state.pep_information.bank_acc_no
    #     collected_doc_info['CreditScore'] = state.pep_information.credit_score

    politico_informatio= {}
    politico_informatio["PEP Expected Response"] = state.pep_information.pep_expected_response
    politico_informatio["Correct Bank Account Number"] = state.pep_information.db_bank_acc_no
    politico_informatio["Correct Credit Score"] = state.pep_information.db_credit_score

    verifier = KYCVerifier(user_personal_information=personal_info, user_document_information=collected_doc_info, politico_informatio=politico_informatio )
    res = verifier.run()
    llm = LLMSingleton().get_llm()
    llm_with_structured_output = llm.with_structured_output(ComparatorState)
    structure_prompt = """You are a KYC verifier. You need to put the following resposne into the corret format.
    {llm_response}"""
    structure_kyc_output_prompt = ChatPromptTemplate(("system", structure_prompt))
    structure_response_chain = structure_kyc_output_prompt | llm_with_structured_output

    final_res = structure_response_chain.invoke({"llm_response": res})
    
    # final_res.kyc_for = personal_info["First Name"]+ " " + personal_info["Last Name"]
    first_name = personal_info.get("First Name", "") or "" 
    last_name = personal_info.get("Last Name", "") or ""
    final_res.kyc_for = f"{first_name} {last_name}".strip()  
    final_res.kyc_type = state.initial_state.kyc_for

    updated_flags = state.flags
    updated_flags.stepper = "4"
    updated_flags.current_conversation_type = final_res.kyc_result

    output = AIMessage(content = "Thank you for your patience, we hereby confirm that your KYC is successful.") if final_res.kyc_result == "Pass" else AIMessage(content = "We regret to inform you that your KYC request has failed.")
    
    print(final_res)
    return {
        "flags": updated_flags,
        "kyc_verifier_state": final_res,  
        "history":[AIMessage(content = res)],
        "output":[output]}

# if __name__ == "__main__":
#     verifier = KYCVerifier()
#     verifier.run()