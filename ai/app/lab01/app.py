from fastapi import APIRouter, Body
# models
from schemas import BOOKS, BookRequest, Book

book = APIRouter(prefix='/api/v1')

@book.get("/books", tags = ["books"])
async def read_all_books():
  return BOOKS

@book.get("/books/{book_id}", tags = ['books'])
async def read_book(book_id: int):
  for book in BOOKS:
    if (book.id == book_id ):
      return book

@book.get("/books/", tags = ['books'])
async def read_book_by_rating(rating: int):
  read_book_rating = []
  for book in BOOKS:
    if (book.rating == rating ):
      read_book_rating.append(book)

  return read_book_rating 


@book.post("/books", tags=["books"])
async def create_book(book_request : BookRequest): 
  new_book = Book(**book_request.dict())
  print(type(new_book))
  BOOKS.append(find_book_id(new_book))


@book.put("/books", tags = ['books'])
async def update_book(book : BookRequest):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book.id:
      BOOKS[i] = book
  
@book.delete("/books/{book_id}", tags = ['books'])  
async def delete_book(book_id : int):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id: 
      BOOKS.pop(i)
      break

def find_book_id(book: Book):
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
  return book