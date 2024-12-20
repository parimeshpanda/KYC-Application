# Common functions used throughout the project
import os

from langchain_openai import AzureChatOpenAI
from src.constants import Constant


class LLMSingleton():
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LLMSingleton, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    

    def initialize(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint= Constant.GPT4_TURBO_ENDPOINT,  # or your deployment
            api_version="2024-05-01-preview",  # or your api version
            azure_deployment=Constant.AZURE_4o_DEPLOYMENT_NAME,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # api_key=client.get_secret("GPT-TURBO-API-KEY").value,
            api_key= Constant.GPT4_TURBO_KEY,
            seed = 42)

    def get_llm(self):
        return self.llm