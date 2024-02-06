from pydantic import BaseModel


class AbstractModel(BaseModel):
    id: str
    # title: str
