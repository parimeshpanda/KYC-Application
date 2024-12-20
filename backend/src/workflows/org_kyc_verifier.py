import os
import json

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import StructuredTool
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage, AIMessage

from src.util.llm_singleton import LLMSingleton
from src.models.agent_state import ComparatorState


USA_ORG_GUIDELINES_NAME= "usa_org_guidelines.txt"

class OrganizationKYCVerifier:
    def __init__(self, org_information, document_information):
        self.org_information = org_information
        self.document_information = document_information
        self.tools = [
            StructuredTool.from_function(self.usa_org_guidelines),
            StructuredTool.from_function(self.org_information_tool),
            StructuredTool.from_function(self.org_doc_information)
        ]
        self.sys_prompt = self._create_system_prompt()
        self.prompt = self._create_prompt()
        self.llm = LLMSingleton().get_llm()   
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    @staticmethod
    def usa_org_guidelines(query: str) -> str:
        """Provide KYC requirements for Private Limited Organizations in the USA."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..','guidelines', USA_ORG_GUIDELINES_NAME)
        # file_path= r"C:\Users\703398752\OneDrive - Genpact\Desktop\Work\dev\LLM-IT\guidelines\usa_org_guidelines.txt"
        with open(file_path, 'r') as file:
            guidelines = str(file.read())
        return guidelines

    def org_information_tool(self, query: str) -> str:
        """Retrieve organization information provided for KYC verification."""
        return f"Organization KYC information provided: {self.org_information}"

    def org_doc_information(self, query: str) -> str:
        """Returns information extracted from uploaded documents."""
        return f"Information extracted from organization documents: {self.document_information}"

    @staticmethod
    def _create_system_prompt() -> str:
        return """FIRST validate that the document information provided by the "org_doc_information" tool matches the organization information provided by "org_information" tool in all common fields.
        Required organization document fields must include:
        - Legal Business Name
        - Organisation Type must be present(Sole Proprietorship/Partnership Firm/Limited Liability Partnership/Private Limited Company/ Public Limited Company)
        - Organisation Location
        - Business License Number
        - Business License Expiry Date
        - Business License Issue Date
        - Issue date of certificate of incorporation
        - Number of board members present
        - Information of all board members present(including Passport/SSN)
        
        Additional requirements:
        1. All matching fields between document and provided information must be EXACTLY matched! Failure to match important information like Name and Document numbers will lead to termination!!
        2. Document information may contain subset of fields but all present fields must match.
        3. Verification fails if any matching field has discrepancy.
        4. Organization country must be mentioned.
        5. All board members must have valid identification.
        6. Issue date of certificate of incorporation  must be valid and active.
        7. Business License issue date and expiry dates must be valid and active.
        8. To fill the final field "user_confirmation" you must display the user with all the information that they have provided and ask user a 'yes' or 'no' question whether they want to update or not. 
        9. STRICLY ASK USER WHETHER HE WANTS TO UPDATE FIELD OR NOT AND IF USER SAYS 'NO' MARK THE USER CONFIRMATION AS 'TRUE'. 
        10. You should collect all the necessary information and none of the field should be "None"
        
        ONLY AND ONLY IF the above step is successful DO THIS: 
        
        Based on the country fetched by the "org_information" tool call the respective country guidelines tool.
        The "org_doc_information" tool might have lesser information, but the key value pairs of the information should EXACTLY match with the info received from "org_information" tool.
        For example, if the country fetched by the information tool is USA, then call the tool "usa_org_guidelines" 
        or if the country fetched by the information tool is Europe, then call the tool "europe_org_guidelines".
        FINALLY Then use the guidelines as a checklist and compare the information entered by the "org_information" tool and check if the information is sufficient and in compliance with the guidelines.
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
            "input": """Verify organization KYC compliance and return:
            1. YES/NO status
            ONYL IF verification failes, Provide:
            1. Detailed reason 
            2. List of any missing or non-compliant items"""
        })
        return result['output']


def verify_org_kyc(state):
    # ORG INFO
    org_info=""
    org_info+= str(state.basic_org_info)
    # org_docs_info = state.all_collected_org_docs
    org_info+=str(state.all_collected_org_docs[0]['Org-BusinessLicense'].doc_information)
    org_info+=str(state.all_collected_org_docs[1]['Org-CertificateofIncorporation'].doc_information)
    # org_info.append(state.all_board_member_information)
    # for i in range(len(state.all_board_member_information)):
    #     org_info.append([i][f'member-{i+1}-doc-info'])
    # state.all_board_member_information.
    
    member_info_list = []
    for i in range(len(state.all_board_member_information)):
        member_info_list.append({})
    for i in range(len(state.all_board_member_information)):
        member_info_list[i][f"member-{i+1}"] = {f"member-info":state.all_board_member_information[i][f"member-{i+1}-info"]}
    org_info+=str(member_info_list)
    print(org_info)
    # DOC INFO : di_extracted_info & member_doc_info_list
    doc_info=""
    member_doc_info_list = []  
    for i in range(len(state.all_board_member_information)):
        member_doc_info_list.append({})
    for i in range(len(state.all_board_member_information)):
        member_doc_info_list[i][f"member-{i+1}"] = {f"member-extracted-doc-info":state.all_board_member_information[i][f"member-{i+1}-doc-info"].extracted_document_information}
    
    di_extracted_info= [{},{}] 
    di_extracted_info[0]=di_extracted_info[0]["Org-BusinessLicense"] = {f"extracted-Org-BusinessLicense":state.all_collected_org_docs[0][f"Org-BusinessLicense"].doc_extracted_info}
    di_extracted_info[1]=di_extracted_info[1]["Org-CertificateofIncorporation"] = {f"extracted-Org-CertificateofIncorporation":state.all_collected_org_docs[1][f"Org-CertificateofIncorporation"].doc_extracted_info}
    doc_info+=str(member_doc_info_list)
    doc_info+= str(di_extracted_info)
    print(doc_info)
    # member_doc_info_list[i][f"member-{i+1}"] = {f"member-extracted-doc-info":state.all_board_member_information[i][f"member-{i+1}-doc-info"].document_information}
    
    # org_info["Organization location"] = state.basic_org_info.org_location
    # org_info["Business Name"] = state.basic_org_info.firm_name
    # org_info["Organization Type"] = state.basic_org_info.firm_name

    verifier = OrganizationKYCVerifier(org_information=org_info, document_information=doc_info)
    res = verifier.run()

    llm = LLMSingleton().get_llm()
    llm_with_structured_output = llm.with_structured_output(ComparatorState)
    structure_prompt = """You are a KYC verifier. You need to put the following resposne into the corret format.
    {llm_response}"""
    structure_kyc_output_prompt = ChatPromptTemplate(("system", structure_prompt))
    structure_response_chain = structure_kyc_output_prompt | llm_with_structured_output

    final_res = structure_response_chain.invoke({"llm_response": res})

    final_res.kyc_type = state.initial_state.kyc_for
    final_res.kyc_for = state.basic_org_info.firm_name
    updated_flags = state.flags
    updated_flags.stepper = "4"
    updated_flags.current_conversation_type = final_res.kyc_result

    print(final_res)
    return {
        "flags": updated_flags,
        "kyc_verifier_state": final_res,
        "history": [AIMessage(content=res)]
    }