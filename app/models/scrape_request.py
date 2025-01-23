from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    page_limit: int = 5
    proxy: str = None  