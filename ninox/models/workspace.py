from pydantic import BaseModel


class Workspace(BaseModel):
    id: str
    name: str
