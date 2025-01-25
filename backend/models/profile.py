from pydantic import BaseModel
from typing import Dict, List, Optional

class Profile(BaseModel):
    name: str
    title: Optional[str] = None
    confidence_score: float
    bio: Optional[str] = None
    sources: Dict[str, str]
    skills: List[str] = []
    location: Optional[str] = None
    
class SearchQuery(BaseModel):
    query: str
    location: Optional[str] = None
    
class SearchResponse(BaseModel):
    profiles: List[Profile] 