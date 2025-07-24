from pydantic import BaseModel

class TaskRequest(BaseModel):
    option: str  # 'cal' or 'crawl'