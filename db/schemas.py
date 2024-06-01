from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    password: str
    kind: str
    highscore: int
    historial: str

class Historial(BaseModel):
    id: int
    user_id: int
    points: int
    
    class Config:
        from_attributes = True