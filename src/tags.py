from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean


# Pydantic schema for validation
class TagSchema(BaseModel):
    name: str
    message: str
    owner: str
    owner_id: str
    key: str

    class Config:
        orm_mode = True
        from_attributes = True

# Pydantic schema for response
class TagResponseSchema(BaseModel):
    name: str
    message: str
    owner_id: str

    class Config:
        orm_mode = True
        from_attributes = True

# Pydantic schema for delete
class DeleteTagSchema(BaseModel):
    key: str

    class Config:
        orm_mode = True
        from_attributes = True