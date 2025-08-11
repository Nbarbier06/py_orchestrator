from pydantic import BaseModel, Field
from typing import Optional, List

class AskRequest(BaseModel):
    query: str = Field(..., min_length=4)
    mode: str = Field("balanced", pattern="^(quick|balanced|deep)$")
    override_urls: Optional[List[str]] = None

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
