from pydantic import BaseModel, Field

class ScrapeRequest(BaseModel):
    page_count: int = Field(..., gt=0)
    proxy_string: str = Field(...)