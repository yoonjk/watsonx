from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel):
    message: str = Field(None, title="Watsonx AI Platform", description="Dict or String?")
    source: Optional[str] = Field(None, title="source language", description="Dict or String?")
    target: Optional[str] = Field(None, title="target language", description="Dict or String?")

class PromptMessage(BaseModel):
    message: str = Field(None, title="Watsonx AI Platform", description="Dict or String?")


