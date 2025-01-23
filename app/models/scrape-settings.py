from pydantic import BaseModel


class ScrapeSettings(BaseModel):
    limit_pages: int
    proxy: str
