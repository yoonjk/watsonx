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
import os
from datetime import timedelta, datetime
from config import getConfig

router = APIRouter(prefix="/api/v1", tags=['auth'])

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/token')

print('Secret-KEY:', SECRET_KEY)


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
  
class Token(BaseModel):
  access_token: str
  token_type: str 
  
def authenticate_user(username: str, password: str, db):
  user = db.query(Users).filter(Users.username == username).first()
  if not user:
    return False
  if not bcrypt_context.verify(password, user.hashed_password):
    return False
  
  return user
    
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
  encode = {'sub': username, 'id': user_id, 'role': role}
  expires = datetime.utcnow() + expires_delta
  
  encode.update({'exp': expires})
  
  return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    user_id: int = payload.get('id')
    user_role: str = payload.get('role')
    
    if username is None or user_id is None:
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, default='Could not validate user.')
    
    return {'username': username, 'id': user_id, 'user_role': user_role}
  except JWTError: 
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, default='Could not validate user.')
  
  
@router.get("/auth/{username}")  
async def find_user(db: db_dependency, username: str):
  user_model = db.query(Users).filter(Users.username == username).first() 
  
  return user_model
 
@router.post("/auth", status_code = status.HTTP_201_CREATED)
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

@router.put('/auth/{username}', status_code = status.HTTP_204_NO_CONTENT)
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
  

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
  user = authenticate_user(form_data.username, form_data.password, db)
  
  if not user:
    return 'Failed Authentication'
  
  token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
  
  return {'access_token': token, 'token_type': 'bearer'}
