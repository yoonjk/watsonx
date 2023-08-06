from fastapi import APIRouter, Body
# models
from schemas import BOOKS, Book

book = APIRouter(prefix='/api/v1')

@book.get("/books", tags = ["books"])
async def read_all_books():
  return BOOKS

@book.post("/books", tags=["books"])
async def create_book(book_request = Body()): 
  BOOKS.append(book_request)