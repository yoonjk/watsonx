from fastapi import APIRouter, Path, HTTPException
# models
from schemas import BOOKS, BookRequest, Book
from starlette import status 

router = APIRouter(prefix='/api/v1')

@router.get("/books", tags = ["books"])
async def read_all_books():
  return BOOKS

@router.get("/books/{book_id}", tags = ['books'], status_code = status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt = 0)):
  for book in BOOKS:
    if (book.id == book_id ):
      return book

@router.get("/books/", tags = ['books'])
async def read_book_by_rating(rating: int):
  read_book_rating = []
  for book in BOOKS:
    if (book.rating == rating ):
      read_book_rating.append(book)

  return read_book_rating 


@router.post("/books", tags=["books"])
async def create_book(book_request : BookRequest): 
  new_book = Book(**book_request.dict())
  print(type(new_book))
  BOOKS.append(find_book_id(new_book))


@router.put("/books", tags = ['books'], status_code = status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
  book_changed = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book.id:
      BOOKS[i] = book
      
  if not book_changed:
    raise HTTPException(status_code = 404, detail = 'Item not found')
  
@router.delete("/books/{book_id}", tags = ['books'], status_code = status.HTTP_204_NO_CONTENT)  
async def delete_book(book_id : int = Path(gt = 0)):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id: 
      BOOKS.pop(i)
      break

  raise HTTPException(status_code = 404, detail = 'Item not found')

def find_book_id(book: Book):
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
  return book