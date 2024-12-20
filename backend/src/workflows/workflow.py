import json
from dotenv import load_dotenv
from fastapi import HTTPException
from redis import Redis
from src.models.model import Userstate
from src.util.redis_setup import RedisCleanup, RedisSaver
from src.workflows.org_kyc_verifier import verify_org_kyc
from src.workflows.organization_kyc import (board_member_assistant, board_member_collector, board_member_doc_info_assistant,board_member_doc_info_collector, 
                                            board_member_doc_upload, board_member_doc_upload_assistant, extract_board_member_info, initialize_state_for_members, 
                                            io_assistant, io_collector, org_collect_doc_info_assistant, org_doc_info_collector, org_doc_upload, org_doc_upload_assistant, 
                                            org_extract_info,org_init_doc_collector, org_questions_assistant, org_questions_collector, update_org_docs_to_collect, 
                                            review_information)
from src.workflows.kyc_with_form import (upload_filled_form, extract_info_from_filled_form,update_state_from_extracted_info, form_doc_upload_assistant, 
                                         upload_form_doc, extract_info_from_form_doc,form_collector_init,update_extracted_form_info_assistant,
                                         update_extracted_form_info_collector,update_state_from_final_information)
from src.workflows.pep_quest import pep_assistant_node,pep_collect_information, extract_pep_info
from src.workflows.org_pep_quest import extract_org_pep_info, org_pep_assistant_node, org_pep_collect_information
from src.config.conn import postgres_checkpointer
load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.graph import END,  StateGraph
from src.models.agent_state import AgentState, APIFlags, ComparatorState, UnifiedUserInformation
from src.models.organization_state import OrganizationState
from src.models.required_information import RequiredInformation
from src.models.retriever_state import RetrieverState
from src.models.doc_collector_state import DocCollectorState
from src.workflows.information_collector import collect_information, assistant_node
from src.services.save_to_db import save_info
from src.workflows.checklist_retriever import guildelines_fetcher
from src.workflows.comparator import compare_info
from src.workflows.collect_docs import doc_assistant_node, doc_information_collection_node, doc_upload_assistant, doc_upload, extract_info, collect_doc_info_assistant, doc_info_collector, init_doc_collector, update_docs_to_collect
from src.tool.document_tools import tool_node
from src.constants import Constant
from sqlalchemy.orm import Session
from src.config.conn import postgres_checkpointer

# checkpointer = RedisSaver(conn=Constant.REDIS_CONN)
checkpointer = postgres_checkpointer()


def individual_or_organization(state:AgentState):
    if state.initial_state.kyc_for != "None" and state.initial_state.kyc_for != None and state.initial_state.user_confirmation == True:
        if state.initial_state.if_kyc_with_uploaded_document == True:
            return "KYC with FORM"
        
        elif state.initial_state.kyc_for == "Individual":
            return "Individual"
        
        elif state.initial_state.kyc_for == "Organization" and state.initial_state.organization_type != "None" and state.initial_state.organization_type != None:
            return "Organization"

        else:
            return "more info required"
    return "more info required"            


def all_details_collected(state: AgentState):
    if (state.retriever_state.checklist_retrieved == False and state.user_information.user_country != 'None') or (state.user_information.user_country != 'None' and state.user_information.user_country_updation == True):
        return "fetch guidelines"
    
    elif state.user_information.user_confirmation == True:
        return "all info collected"
    
    else:
        return "more info required"

def pep_details_collected(state: AgentState):
    if state.pep_information.political_exposure != 'None' and state.pep_information.bank_acc_no != 'None' and state.pep_information.credit_score != 'None' and state.pep_information.political_exposure != None and state.pep_information.bank_acc_no != None and state.pep_information.credit_score != None:
        return "call comparator"
    
    else:
        return "more info required"

def is_pep(state:AgentState):
    if(state.pep_information.pep_extracted_db==True):
        return "pep detected"
    else:
        return "pep not detected"

def if_docs_selected(state: AgentState) -> str:
    # if state.doc_collector_state.selected_doc1 != None and state.doc_collector_state.selected_doc2 != None and state.doc_collector_state.selected_doc1 != "None" and state.doc_collector_state.selected_doc2 != "None":
    if state.doc_collector_state.selected_doc1 != None and state.doc_collector_state.selected_doc1 != 'None':
        return "All docs selected"
    return "Select docs"

def doc_upload_condition(state:AgentState):
    if state.doc_collector_state.if_doc1_uploaded == None or state.doc_collector_state.if_doc1_uploaded == False:
        return "Document not uploaded"
    return "Doc uploaded"

def collect_doc_info_condition(state:AgentState):
    if state.doc_collector_state.doc1_information['user_confirmation'] == True:
        return "All Doc Info Collected"
    return "More Info required"

def if_all_docs_collected(state:AgentState):
    for i in state.docs_to_collect:
        if i['collected'] == False:
            return "More docs required"
    return "All docs collected"

def extract_info_condition(state:AgentState):
    if state.doc_collector_state.doc1_verification == True:
        return "Verified"
    return "Failed verification"

def if_optional_documents(state:AgentState):
    if len(state.doc_collector_state.model_json_schema()['properties']['selected_doc1']['anyOf'][0]['enum']) > 2:
        return "Optional Documents"
    return "Mandatory Document"

def if_org_details_collected(state:AgentState):
    if state.basic_org_info != None and state.basic_org_info.user_confirmation == True:
        return "all info collected"
    return "more info required"

def if_org_member_details_collected(state:AgentState):
    # if state.organization_state.current_member_info.user_confirmation == True and state.organization_state.num_board_members_collected == state.organization_state.basic_org_info.num_firm_members:
    #     return "all_member_info_collected"
    
    if state.current_member_info.user_confirmation == True:
        return "member_info_collected"
    return "more info required"

def if_org_member_doc_uploaded(state:AgentState):
    if state.current_member_doc_info.doc_uploaded == True: 
        return "member doc uploaded"
    return "doc not uploaded"

def if_org_member_info_extracted(state:AgentState):
    # if state.organization_state.current_member_doc_info.extracted_document_information != None and state.organization_state.num_board_members_collected == state.organization_state.basic_org_info.num_firm_members:
    #     return "all member info extracted"
    if state.current_member_doc_info.extracted_document_information != None:
        return "extracted info"
    return "could not extract info"

def if_org_member_doc_info_collected(state:AgentState):
    if state.current_member_doc_info.document_information['user_confirmation'] == True and state.num_board_members_collected >= state.basic_org_info.num_firm_members:
        return "all doc info collected"
    elif state.current_member_doc_info.document_information['user_confirmation'] == True:
        return "member doc info collected"
    return "more doc info required"

def is_org_risky(state:AgentState):
    if state.org_pep_information.high_risk_factor_db == True:
        return "risky"
    else:
        return "not risky"
    
def org_pep_details_collected(state: AgentState):
    if state.org_pep_information.annual_revenue != 'None' and state.org_pep_information.pep_members != 'None' and state.org_pep_information.dividends_pq != 'None' and state.org_pep_information.annual_revenue != None and state.org_pep_information.pep_members != None and state.org_pep_information.dividends_pq != None:
        return "call comparator"
    else:
        return "more info required"

def org_doc_upload_condition(state:AgentState):
    if state.org_doc_collector_state.if_doc_uploaded == None or state.org_doc_collector_state.if_doc_uploaded == False:
        return "Document not uploaded"
    return "Doc uploaded"

def org_extract_info_condition(state:AgentState):
    if state.org_doc_collector_state.doc_verification == True:
        return "Verified"
    return "Failed verification"

def org_collect_doc_info_condition(state:AgentState):
    if state.org_doc_collector_state.doc_information['user_confirmation'] == True:
        return "All Doc Info Collected"
    return "More Info required"

def org_if_all_docs_collected(state:AgentState):
    for i in state.org_docs_to_collect:
        if i['collected'] == False:
            return "More docs required"
    return "All docs collected"

def if_all_form_info_collected(state:AgentState):
    if state.doc_collector_state.doc1_verification == True:
        return "All info collected"
    return "more info required"

def if_all_form_fields_updated(state:AgentState):
    if state.filled_form_extracted_structured_info.user_confirmation == True:
        return "All info collected"
    return "More info required"


def if_all_form_docs_collected(state:AgentState):
    num_docs_to_collect = 0
    for i in state.docs_to_collect:
        if i['collected'] == False:
            num_docs_to_collect += 1

    if num_docs_to_collect == 0:
        return "All Docs Collected"
    return "More Docs Required"

workflow = StateGraph(AgentState)
workflow.add_node(Constant.ASSISTANT, assistant_node)
workflow.add_node(Constant.COLLECT_INFO, collect_information)
workflow.add_node(Constant.SAVE_INFO, save_info)
workflow.add_node(Constant.GUIDELINES_FETCHER, guildelines_fetcher)
workflow.add_node(Constant.INIT_DOC_COLLECTOR,init_doc_collector)
workflow.add_node(Constant.DOC_ASSISTANT, doc_assistant_node)
workflow.add_node(Constant.COLLECT_DOC_INFO,doc_information_collection_node)
workflow.add_node(Constant.DOC_UPLOAD_ASSISTANT,doc_upload_assistant)
workflow.add_node(Constant.DOC_UPLOAD,doc_upload)
workflow.add_node(Constant.EXTRACT_INFO_FROM_DOC,extract_info)    
workflow.add_node(Constant.DOC_INFO_ASSISTANT,collect_doc_info_assistant)
workflow.add_node(Constant.DOC_INFO_COLLECTOR,doc_info_collector)
workflow.add_node(Constant.UPDATE_DOCS_TO_COLLECT, update_docs_to_collect)
workflow.add_node(Constant.PEP_EXTRACTOR, extract_pep_info)
workflow.add_node(Constant.PEP_INFO, pep_assistant_node)
workflow.add_node(Constant.PEP_COLLECT_INFO, pep_collect_information)
workflow.add_node(Constant.COMPARATOR, compare_info)

workflow.add_node(Constant.ORG_QUES_ASSISTANT, org_questions_assistant)
workflow.add_node(Constant.ORG_QUES_COLLECTOR, org_questions_collector)
workflow.add_node(Constant.ORG_INIT_MEMBER_STATE, initialize_state_for_members)
workflow.add_node(Constant.ORG_MEMBER_QUES_ASSISTANT, board_member_assistant)
workflow.add_node(Constant.ORG_MEMBER_QUES_COLLECTOR, board_member_collector)
workflow.add_node(Constant.ORG_MEMBER_DOC_UPLOAD_ASSISTANT, board_member_doc_upload_assistant)
workflow.add_node(Constant.ORG_MEMBER_DOC_UPLOAD, board_member_doc_upload)
workflow.add_node(Constant.ORG_MEMBER_EXTRACT_INFO,extract_board_member_info)
workflow.add_node(Constant.ORG_MEMBER_DOC_INFO_ASSISTANT, board_member_doc_info_assistant)
workflow.add_node(Constant.ORG_MEMBER_DOC_INFO_COLLECTOR, board_member_doc_info_collector)

# workflow.add_node(ORG_DOC_COLLECTOR_ASSISTANT,org_doc_collector_assistant)
# workflow.add_node(ORG_COLLECT_DOC_INFO,org_doc_information_collection_node)
workflow.add_node(Constant.ORG_DOC_UPLOAD,org_doc_upload)
workflow.add_node(Constant.ORG_DOC_UPLOAD_ASSISTANT,org_doc_upload_assistant)
workflow.add_node(Constant.ORG_DOC_INFO_ASSISTANT,org_collect_doc_info_assistant)
workflow.add_node(Constant.ORG_DOC_INFO_COLLECTOR,org_doc_info_collector)
workflow.add_node(Constant.ORG_EXTRACT_INFORMATION,org_extract_info)
workflow.add_node(Constant.INIT_ORG_DOC_COLLECTOR,org_init_doc_collector)
workflow.add_node(Constant.UPDATE_ORG_DOCS_TO_COLLECT,update_org_docs_to_collect)
workflow.add_node(Constant.ORG_PEP_EXTRACTOR,extract_org_pep_info)
workflow.add_node(Constant.ORG_PEP_INFO,org_pep_assistant_node)
workflow.add_node(Constant.ORG_PEP_COLLECT_INFO,org_pep_collect_information)
workflow.add_node(Constant.ORG_COMPARATOR,verify_org_kyc)

workflow.add_node(Constant.REVIEW_INFO, review_information)

workflow.add_node(Constant.IO_ASSISTANT, io_assistant)   
workflow.add_node(Constant.IO_COLLECTOR, io_collector) 

workflow.add_node(Constant.UPLOAD_FILLED_FORM ,upload_filled_form)
workflow.add_node(Constant.EXTRACT_INFO_FROM_FORM ,extract_info_from_filled_form)
workflow.add_node(Constant.UPDATE_STATE_FROM_FORM ,update_state_from_extracted_info)
workflow.add_node(Constant.UPDATE_EXTRACTED_INFO_ASSISTANT,update_extracted_form_info_assistant)
workflow.add_node(Constant.UPDATE_EXTRACTED_INFO_COLLECTOR,update_extracted_form_info_collector)
workflow.add_node(Constant.UPDATE_STATE_WITH_CONFIRMED_INFORMATION, update_state_from_final_information)
workflow.add_node(Constant.FORM_DOC_UPLOAD_ASSISTANT ,form_doc_upload_assistant)
workflow.add_node(Constant.UPLOAD_FORM_DOCS ,upload_form_doc)
workflow.add_node(Constant.EXTRACT_INFO_FROM_FORM_DOC ,extract_info_from_form_doc)
workflow.add_node(Constant.FORM_COLLECTOR_INIT, form_collector_init)
# Init
workflow.set_entry_point(Constant.IO_ASSISTANT)
workflow.add_edge(Constant.IO_ASSISTANT, Constant.IO_COLLECTOR)
workflow.add_conditional_edges(Constant.IO_COLLECTOR, individual_or_organization, {"KYC with FORM":Constant.UPLOAD_FILLED_FORM,"Individual":Constant.ASSISTANT, "Organization":Constant.ORG_QUES_ASSISTANT, "more info required":Constant.IO_ASSISTANT})

# KYC with form
workflow.add_edge(Constant.UPLOAD_FILLED_FORM, Constant.EXTRACT_INFO_FROM_FORM)
workflow.add_edge(Constant.EXTRACT_INFO_FROM_FORM, Constant.UPDATE_STATE_FROM_FORM)
workflow.add_edge(Constant.UPDATE_STATE_FROM_FORM,Constant.UPDATE_EXTRACTED_INFO_ASSISTANT )

workflow.add_edge(Constant.UPDATE_EXTRACTED_INFO_ASSISTANT, Constant.UPDATE_EXTRACTED_INFO_COLLECTOR)
workflow.add_conditional_edges(Constant.UPDATE_EXTRACTED_INFO_COLLECTOR,if_all_form_fields_updated,{"All info collected":Constant.UPDATE_STATE_WITH_CONFIRMED_INFORMATION , "More info required":Constant.UPDATE_EXTRACTED_INFO_ASSISTANT})
workflow.add_edge(Constant.UPDATE_STATE_WITH_CONFIRMED_INFORMATION, Constant.FORM_DOC_UPLOAD_ASSISTANT)
workflow.add_edge(Constant.FORM_DOC_UPLOAD_ASSISTANT, Constant.UPLOAD_FORM_DOCS)
workflow.add_edge(Constant.UPLOAD_FORM_DOCS, Constant.EXTRACT_INFO_FROM_FORM_DOC)
workflow.add_conditional_edges(Constant.EXTRACT_INFO_FROM_FORM_DOC, if_all_form_info_collected, {"All info collected":Constant.FORM_COLLECTOR_INIT,"more info required":Constant.FORM_DOC_UPLOAD_ASSISTANT})

# workflow.add_conditional_edges(Constant.FORM_COLLECTOR_INIT, if_all_form_docs_collected, {"All Docs Collected":Constant.REVIEW_INFO, "More Docs Required":Constant.FORM_DOC_UPLOAD_ASSISTANT})
workflow.add_conditional_edges(Constant.FORM_COLLECTOR_INIT, if_all_form_docs_collected, {"All Docs Collected":Constant.PEP_EXTRACTOR, "More Docs Required":Constant.FORM_DOC_UPLOAD_ASSISTANT})
# workflow.add_edge(Constant.REVIEW_INFO, Constant.COMPARATOR)

# For Individuals 
workflow.add_edge(Constant.ASSISTANT,Constant.COLLECT_INFO)
workflow.add_conditional_edges(Constant.COLLECT_INFO, all_details_collected, {"all info collected": Constant.INIT_DOC_COLLECTOR, "more info required": Constant.ASSISTANT, "fetch guidelines":Constant.GUIDELINES_FETCHER})
workflow.add_conditional_edges(Constant.INIT_DOC_COLLECTOR,if_optional_documents, {"Optional Documents":Constant.DOC_ASSISTANT, "Mandatory Document":Constant.DOC_UPLOAD_ASSISTANT})
workflow.add_edge(Constant.GUIDELINES_FETCHER,Constant. ASSISTANT)
workflow.add_edge(Constant.DOC_ASSISTANT,Constant. COLLECT_DOC_INFO)
workflow.add_edge(Constant.DOC_UPLOAD_ASSISTANT,Constant. DOC_UPLOAD)
workflow.add_edge(Constant.DOC_INFO_ASSISTANT, Constant.DOC_INFO_COLLECTOR)
workflow.add_conditional_edges(Constant.COLLECT_DOC_INFO,if_docs_selected, {"All docs selected":Constant.DOC_UPLOAD_ASSISTANT, "Select docs":Constant.DOC_ASSISTANT})
workflow.add_conditional_edges(Constant.DOC_UPLOAD, doc_upload_condition, {"Document not uploaded":Constant.DOC_UPLOAD_ASSISTANT, "Doc uploaded":Constant.EXTRACT_INFO_FROM_DOC})
workflow.add_conditional_edges(Constant.EXTRACT_INFO_FROM_DOC, extract_info_condition,{"Failed verification":Constant.DOC_UPLOAD_ASSISTANT, "Verified":Constant.DOC_INFO_ASSISTANT})
workflow.add_conditional_edges(Constant.DOC_INFO_COLLECTOR,collect_doc_info_condition, {"All Doc Info Collected":Constant.UPDATE_DOCS_TO_COLLECT, "More Info required":Constant.DOC_INFO_ASSISTANT})
workflow.add_conditional_edges(Constant.UPDATE_DOCS_TO_COLLECT, if_all_docs_collected, {"All docs collected":Constant.PEP_EXTRACTOR, "More docs required":Constant.INIT_DOC_COLLECTOR})
# workflow.add_conditional_edges(Constant.UPDATE_DOCS_TO_COLLECT, if_all_docs_collected, {"All docs collected":Constant.REVIEW_INFO, "More docs required":Constant.INIT_DOC_COLLECTOR})
# workflow.add_edge(Constant.REVIEW_INFO, Constant.PEP_EXTRACTOR)
workflow.add_conditional_edges(Constant.PEP_EXTRACTOR, is_pep, {"pep detected":Constant.PEP_INFO, "pep not detected":Constant.REVIEW_INFO})
workflow.add_edge(Constant.PEP_INFO, Constant.PEP_COLLECT_INFO)
workflow.add_conditional_edges(Constant.PEP_COLLECT_INFO, pep_details_collected, {"call comparator":Constant.REVIEW_INFO, "more info required":Constant.PEP_INFO})
workflow.add_edge(Constant.REVIEW_INFO, Constant.COMPARATOR)

# TODO: For Organizations 
workflow.add_edge(Constant.ORG_QUES_ASSISTANT, Constant.ORG_QUES_COLLECTOR)
# workflow.add_conditional_edges(ORG_QUES_COLLECTOR, if_org_details_collected, {"all info collected":ORG_INIT_MEMBER_STATE, "more info required" :ORG_QUES_ASSISTANT})
workflow.add_conditional_edges(Constant.ORG_QUES_COLLECTOR, if_org_details_collected, {"all info collected":Constant.INIT_ORG_DOC_COLLECTOR, "more info required" :Constant.ORG_QUES_ASSISTANT})
workflow.add_edge(Constant.INIT_ORG_DOC_COLLECTOR, Constant.ORG_DOC_UPLOAD_ASSISTANT)
workflow.add_edge(Constant.ORG_DOC_UPLOAD_ASSISTANT, Constant.ORG_DOC_UPLOAD)
workflow.add_conditional_edges(Constant.ORG_DOC_UPLOAD,org_doc_upload_condition, {"Document not uploaded":Constant.ORG_DOC_UPLOAD_ASSISTANT, "Doc uploaded": Constant.ORG_EXTRACT_INFORMATION})
workflow.add_conditional_edges(Constant.ORG_EXTRACT_INFORMATION, org_extract_info_condition, {"Verified": Constant.ORG_DOC_INFO_ASSISTANT, "Failed verification": Constant.ORG_DOC_UPLOAD_ASSISTANT} )
workflow.add_edge(Constant.ORG_DOC_INFO_ASSISTANT, Constant.ORG_DOC_INFO_COLLECTOR)
workflow.add_conditional_edges(Constant.ORG_DOC_INFO_COLLECTOR, org_collect_doc_info_condition,{"All Doc Info Collected":Constant.UPDATE_ORG_DOCS_TO_COLLECT, "More Info required":Constant.ORG_DOC_INFO_ASSISTANT})
workflow.add_conditional_edges(Constant.UPDATE_ORG_DOCS_TO_COLLECT, org_if_all_docs_collected,{"All docs collected":Constant.ORG_INIT_MEMBER_STATE,"More docs required": Constant.INIT_ORG_DOC_COLLECTOR })

workflow.add_edge(Constant.ORG_INIT_MEMBER_STATE,Constant. ORG_MEMBER_QUES_ASSISTANT)
workflow.add_edge(Constant.ORG_MEMBER_QUES_ASSISTANT, Constant.ORG_MEMBER_QUES_COLLECTOR)
workflow.add_conditional_edges(Constant.ORG_MEMBER_QUES_COLLECTOR, if_org_member_details_collected, {"member_info_collected":Constant.ORG_MEMBER_DOC_UPLOAD_ASSISTANT, "more info required":Constant.ORG_MEMBER_QUES_ASSISTANT})
workflow.add_edge(Constant.ORG_MEMBER_DOC_UPLOAD_ASSISTANT,Constant. ORG_MEMBER_DOC_UPLOAD)
workflow.add_conditional_edges(Constant.ORG_MEMBER_DOC_UPLOAD, if_org_member_doc_uploaded, {"doc not uploaded":Constant.ORG_MEMBER_DOC_UPLOAD_ASSISTANT, "member doc uploaded": Constant.ORG_MEMBER_EXTRACT_INFO})
workflow.add_conditional_edges(Constant.ORG_MEMBER_EXTRACT_INFO, if_org_member_info_extracted, {"could not extract info":Constant.ORG_MEMBER_DOC_UPLOAD_ASSISTANT, "extracted info":Constant.ORG_MEMBER_DOC_INFO_ASSISTANT})
workflow.add_edge(Constant.ORG_MEMBER_DOC_INFO_ASSISTANT,Constant. ORG_MEMBER_DOC_INFO_COLLECTOR)
workflow.add_conditional_edges(Constant.ORG_MEMBER_DOC_INFO_COLLECTOR,if_org_member_doc_info_collected, {"member doc info collected":Constant.ORG_INIT_MEMBER_STATE, "more doc info required":Constant.ORG_MEMBER_DOC_INFO_ASSISTANT, "all doc info collected":Constant.ORG_PEP_EXTRACTOR})
workflow.add_conditional_edges(Constant.ORG_PEP_EXTRACTOR, is_org_risky, {"risky":Constant.ORG_PEP_INFO, "not risky":Constant.ORG_COMPARATOR})
workflow.add_edge(Constant.ORG_PEP_INFO, Constant.ORG_PEP_COLLECT_INFO)
workflow.add_conditional_edges(Constant.ORG_PEP_COLLECT_INFO, org_pep_details_collected, {"call comparator":Constant.ORG_COMPARATOR, "more info required":Constant.ORG_PEP_INFO})
workflow.add_edge(Constant.ORG_COMPARATOR,Constant.SAVE_INFO)

workflow.add_edge(Constant.COMPARATOR,Constant.SAVE_INFO)
workflow.add_edge(Constant.SAVE_INFO, END)  

interrupt_before_list = [Constant.IO_COLLECTOR ,Constant.COLLECT_INFO, Constant.COLLECT_DOC_INFO, Constant.PEP_COLLECT_INFO, Constant.DOC_INFO_COLLECTOR, Constant.ORG_QUES_COLLECTOR, Constant.ORG_DOC_INFO_COLLECTOR, Constant.ORG_MEMBER_QUES_COLLECTOR, Constant.ORG_MEMBER_DOC_INFO_COLLECTOR, Constant.ORG_PEP_COLLECT_INFO, Constant.UPDATE_EXTRACTED_INFO_COLLECTOR]
interrupt_after_list = [Constant.DOC_UPLOAD, Constant.ORG_DOC_UPLOAD, Constant.ORG_MEMBER_DOC_UPLOAD, Constant.REVIEW_INFO, Constant.UPLOAD_FILLED_FORM, Constant.UPLOAD_FORM_DOCS]
graph = workflow.compile(interrupt_before = interrupt_before_list,
                         interrupt_after = interrupt_after_list,
                         checkpointer= checkpointer)
# graph = workflow.compile(checkpointer= checkpointer)


# graph.get_graph().draw_mermaid()
# graph.get_graph().draw_mermaid_png(output_file_path="graph15.png")

req_info_obj = RequiredInformation(user_country='None', user_name=None, user_ssn = None, user_passport_no=None, user_confirmation=False)

default_state ={"flags": APIFlags(stepper="0", 
                                  current_conversation_type ="conversation"),
                "kyc_verifier_state":ComparatorState(),
                "file_sas_url": None,
                "run_graph":True, 
                "user_information":req_info_obj, 
                "retriever_state":RetrieverState(), 
                "doc_collector_state":DocCollectorState(), 
                "docs_to_collect":  [{"doc": ["SSN","Passport","None"], 
                                      "collected":False}],
                "filled_form_extracted_structured_info":UnifiedUserInformation(),  }


  
def save_req_object(db:Session,config):
    try:
        user_info = graph.get_state(config).values['user_information']
      
        json_data = user_info.json()
        data = Userstate(
            thread_id = config["configurable"]["thread_id"],
            state_obj = json_data
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        print("User info saved successfully.")
    except Exception as e:
        db.rollback()  # Rollback in case of error
        print(f"Error saving user info: {e}")

def human_msg_update(user_input : str,config):
    graph.update_state(config, {"user_input":user_input})


def run_graph(config):
    graph.invoke(default_state, config)
    graph_state =graph.get_state(config).values
    return {"response":str(graph_state['output'][-1].content),
            "stepper": graph_state['flags'].stepper,
            "conversation_type": graph_state['flags'].current_conversation_type,\
            "comparator_state": graph_state['kyc_verifier_state'].model_dump()}

thread_id = 99795
def re_run_graph(user_input : str,config):
    try:
            
        thread_id = config["configurable"]["thread_id"]
  
        human_msg_update(user_input,config)

        graph.invoke(None, config)

        graph_state = graph.get_state(config).values

        ai_question = graph_state['output'][-1].content
        stepper = graph_state['flags'].stepper
        conversation_type = graph_state['flags'].current_conversation_type
        comparator_state = (graph_state['kyc_verifier_state']).model_dump()

        return {"response":ai_question,
                "stepper": stepper,
                "conversation_type": conversation_type,
                "comparator_state": comparator_state}
    except Exception as e:
         raise  HTTPException(status_code=500, detail=str(e))