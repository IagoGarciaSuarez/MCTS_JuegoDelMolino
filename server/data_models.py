from pydantic import BaseModel
from typing import Optional

class NewGame(BaseModel):
    username: str
    game_name: str
    password: str

class Movement(BaseModel):
    initial_pos: Optional[list] = None
    final_pos: list
    kill_tile: Optional[list] = None

class Credentials(BaseModel):
    username: str
    password: str