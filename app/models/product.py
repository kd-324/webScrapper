from pydantic import BaseModel, Field

class Product(BaseModel):
    product_title: str = Field(...)
    product_price: float = Field(..., gt=0)
    path_to_image: str = Field(None)
