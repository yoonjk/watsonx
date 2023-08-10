from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel 
from models import Users 
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session 
from database import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
from .auth import get_current_user
from models import Todos

router = APIRouter(prefix="/api/v1", tags=['admin'])

def get_db():
  db = SessionLocal() 
  
  try:
    yield db
  finally:
    db.close()
  
db_dependency = Annotated[Session, Depends(get_db)]  
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code = status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
  if user is None or user.get('user_role') != 'admin':
    raise HTTPException(status_code = 401, detail = 'Authentication Failed')
  
  return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id:int):
  if user is None or user.get('user_role') != 'admin':
    raise HTTPException(status_code = 401, detail = 'Authentication Failed') 
	
  todo_model = db.query(Todos).filter(Todos.id == todo_id).delete()
  db.commit()