from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage

from src.models.agent_state import AgentState
from src.models.retriever_state import RetrieverState
from src.util.llm_singleton import LLMSingleton
from src.constants import Constant
llm = LLMSingleton().get_llm()

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint= Constant.EMBEDDING_API_ENDPOINT,  # or your deployment
    api_version="2024-05-01-preview", 
    # api_key=client.get_secret("EMBEDDING-API-KEY").value,
    api_key=Constant.EMBEDDING_KEY,
    azure_deployment=Constant.EMBEDDING_DEPLOYMENT_NAME
)

guidelines_prompt = """ Your job is to provide a list of documents, that will be required by the user to validate the checklist. The user is from {country}.
You Only Need to provide the Names of the documents required by the user.There is No Need to provide the any reason or additional information. Use the example given below as reference.

<example>
Use the following example as reference:
**EXAMPLE CHECKLIST**
<China Guidelines>
- The First Name and Last Name entered by the user should match with the Birth Certificate of the User.
- The Social Credits entered by the user should be the same as the ones in the Social Credits Card Provided by the user.
</China Guidelines>

**EXAMPLE RESPONSE**
Just a heads up!
Please be ready with the a copy of the following documents, as they will be requried during the KYC process.
    - Birth Certificate
    - Social Credits Card
</example>

The checklist to be validated is given below:
**Checklist**
{checklist}
"""

retriever_prompt = ChatPromptTemplate([
    ("system","You are a hepful assistant, that helps with KYC verification of users."),
    ("human", guidelines_prompt)])


# Can't get what documents were retrieved
# chain = (
#     {"checklist": retriever, "country": RunnablePassthrough()}
#     | retriever_prompt
#     | llm
# )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def guildelines_fetcher(state: AgentState):

    # retrieve_docs = (lambda x: x["input"]) | retriever
    
    # rag_chain = (
    # {"country": lambda x: x["input"],
    # "checklist": lambda x: format_docs(x["context"])}
    # | guidelines_prompt
    # | llm)

    user_country = state.user_information.user_country


    # docs = retriever.invoke(user_country)
    # chain = retriever_prompt | llm
    
    # res = chain.invoke({"checklist":format_docs(docs), "country":user_country})
    res = AIMessage("CHECKLISTS ARE TO BE RETRIEVED")
    retriever_state = RetrieverState(checklist_retrieved=True , retrieved_checkpoints= ['DOCS ARE TO BE RETRIEVED'])

    user_information = state.user_information
    # user_information.user_country_updation = False
    return({
        "output":[res],
        "retriever_state": retriever_state,
        "user_information": user_information
    })

