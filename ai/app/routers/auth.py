from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel 
from models import Users 
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session 
from database import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/v1")

bcrypt_context = CryptContext(["sha256_crypt"])

def get_db():
  db = SessionLocal() 
  
  try:
    yield db
  finally:
    db.close()
  
db_dependency = Annotated[Session, Depends(get_db)] 

class CreateUserRequest(BaseModel):
  username: str
  email: str
  first_name: str
  last_name: str
  password: str
  role: str
  
def authenticate_user(username: str, password: str, db):
  user = db.query(Users).filter(Users.username == username).first()
  if not user:
    return False
  if not bcrypt_context.verify(password, user.hashed_password):
    return False
  return True
    
@router.get("/auth/{username}", tags=['users'])  
async def find_user(db: db_dependency, username: str):
  user_model = db.query(Users).filter(Users.username == username).first() 
  
  return user_model
 
@router.post("/auth", tags=['users'], status_code = status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
  create_user_model = Users(
		email=create_user_request.email,
    username=create_user_request.username,
    first_name=create_user_request.first_name,
    last_name=create_user_request.last_name,
    role=create_user_request.role,
    hashed_password=bcrypt_context.hash(create_user_request.password),
    is_active=True
	)
  
  db.add(create_user_model)
  db.commit() 

@router.put('/auth/{username}', tags=['users'], status_code = status.HTTP_204_NO_CONTENT)
async def update_user(db: db_dependency,
                      update_user_request: CreateUserRequest,
                      username: str):
  user_model = db.query(Users).filter(Users.username == username).first()
  
  if not user_model:
    raise HTTPException(status_code = 404, detail = 'User not found')
  
  user_model.first_name = update_user_request.first_name 
  user_model.last_name = update_user_request.last_name 
  user_model.email = update_user_request.email 
  user_model.hashed_password = bcrypt_context.hash(update_user_request.password)
  user_model.role = update_user_request.role 
  
  db.add(user_model)
  db.commit()
  

@router.post("/token", tags=['users'])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
  user = authenticate_user(form_data.username, form_data.password, db)
  
  if not user:
    return 'Failed Authentication'
  return 'Successful Authentication'
