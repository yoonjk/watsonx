from pydantic import BaseModel, Field
from typing import Optional
class Message(BaseModel):
    message: str = Field(None, title="Watsonx AI Platform")
    source: Optional[str]
    target: Optional[str]

class PromptMessage(BaseModel):
    message: str = Field(None, title="Watsonx AI Platform")


