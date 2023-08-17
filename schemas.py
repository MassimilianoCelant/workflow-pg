from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id:        Optional[int] = 0
    full_name: str
    email:     str
    username:  str
    password:  str


class Message(BaseModel):
    id: Optional[int] = 0
    user_id: Optional[int] = 0
    text: str
