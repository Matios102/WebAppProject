from pydantic import BaseModel

class CategoryUpdate(BaseModel):
    category_id: int
    category_name: str

class CategoryCreate(BaseModel):
    category_name: str