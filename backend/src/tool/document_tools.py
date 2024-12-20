import os

from typing import Literal, Annotated

from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool 
from langgraph.prebuilt import InjectedState
from langchain_core.runnables import RunnableConfig



def check_for_file_in_directory(file_path: str ) -> bool:
    """Check if the file exists in the given path"""
    return os.path.exists(file_path)

## 
@tool
def check_doc_upload(file_path: str, state: Annotated[dict, InjectedState], config: RunnableConfig):
    """Call to check whether the user has uploaded the documents or not"""
    # file_path = None
    if check_for_file_in_directory(file_path):
        print("File exists")
    else:
        print("File does not exist")


tools = [check_doc_upload]

tool_node = ToolNode(tools=tools)