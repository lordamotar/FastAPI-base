from pydantic import BaseModel
from pydantic import ConfigDict


class ItemBase(BaseModel):
    title: str


class ItemCreate(ItemBase):
    owner_id: int


class ItemOut(ItemBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


