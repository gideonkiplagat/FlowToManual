from pydantic import BaseModel, Field
from typing import List, Any, Optional

class SessionSchema(BaseModel):
    events: List[Any]
    name: Optional[str] = Field(None, max_length=100)
    user_id: Optional[int] = None