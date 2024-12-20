# Common functions used throughout the project
import os
from dotenv import load_dotenv
from typing import List, Union


from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from src.models.doc_collector_state import DocCollectorState

load_dotenv()


def trimmed_history(history:List[BaseMessage])->List[BaseMessage]:
    trimmed_history = []
    for message in history:
        if isinstance(message, HumanMessage):
            trimmed_history.append(message) 
        else:
            trimmed_history.append(AIMessage(content=message.content))

    return trimmed_history



def combine_required_info(old_info:Union[dict, DocCollectorState], new_info:Union[dict,DocCollectorState])->dict:
    if type(old_info) != dict:
        old_info_dict = old_info.__dict__
    else:
        old_info_dict = old_info

    if type(new_info) != dict:
        new_info_dict = new_info.__dict__
    else:
        new_info_dict = new_info

    old_info_dict.update({k: v for k,v in new_info_dict.items() if v != None})
    # new_info_object = DocCollectorState(**old_info_dict)
    
    return old_info_dict


def get_next_doc_to_collect(requried_docs:List[dict]):
    for doc in requried_docs:
        if doc['collected'] == False:
            return doc['doc']
    return None 
