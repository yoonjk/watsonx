from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# postgresql
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin1234@localhost/todoapp'
# mysql
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:1234qwer@localhost:3306/demo'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base() 
