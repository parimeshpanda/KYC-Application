from typing import Optional, Literal

from pydantic import BaseModel,Field



class RetrieverState(BaseModel):
    retrieved_checkpoints: list = Field(default=None)
    checklist_retrieved: bool = Field(default=False)