from pydantic import BaseModel

class News(BaseModel):
    title: str
    body: str
    rating: int
    author: str
