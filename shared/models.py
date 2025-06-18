from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderRequest(BaseModel):
    user_id: str
    items: List[OrderItem]
