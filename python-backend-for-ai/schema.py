from pydantic import BaseModel

class EditCommand(BaseModel):
    command: str
