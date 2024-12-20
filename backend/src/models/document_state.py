# import operator

# from langchain_core.pydantic_v1 import BaseModel, Field
# # from pydantic import BaseModel,Field
# from langgraph.graph import add_messages
# from langchain_core.messages import BaseMessage


# class UploadedDocuments(BaseModel):
#     adhar_card: bool = Field(
#         description="Weather the user has uploaded the adhar card or not.", default=False)

#     passport: bool = Field(
#         description="Weather the user has uploaded the passport or not.", default=False)


# class DocumentState(BaseModel):
#     required_documents: UploadedDocuments