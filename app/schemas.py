from pydantic import BaseModel

class News(BaseModel):
    title: str
    body: str
    rating: int

class UserBase(BaseModel):
    username: str
    password: str
