from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel):
    message: str = Field(None, title="Watsonx AI Platform", description="Dict or String?")
    source: Optional[str] = Field(None, title="source language", description="Dict or String?")
    target: Optional[str] = Field(None, title="target language", description="Dict or String?")

class PromptMessage(BaseModel):
    message: str = Field(None, title="Watsonx AI Platform", description="Dict or String?")


class Book:
    id: int
    title: str 
    author: str
    description: str
    rating: str
    
    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description 
        self.rating = rating 

BOOKS = [
    Book(1, 'Computer Science Pro', 'coding', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'coding', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'coding', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author1', 'Book Description', 2),
    Book(5, 'HP1', 'Author2', 'Book Description', 3), 
    Book(6, 'HP2', ' Author3', 'Book Description', 1) 
]

class BookRequest(BaseModel):
    id: int
    title: str = Field(title='id is not needed', min_length = 3)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 10)
    rating: int = Field(gt = 0, le = 5)

    class Config: 
        schema_extra = {
            'example': {
                'id' : 0,
                'title' : 'A new book',
                'author' : 'coding', 
                'description' : 'A new description of a book',
                'rating' : 5
            }
        }


