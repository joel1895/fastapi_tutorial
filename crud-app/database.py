from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}

) #Establishes the connection to database

SessionLocal = sessionmaker(bind=engine, autoflush=False,autocommit=False) #Creates new db session

Base = declarative_base() #creates base class for models to inherit from,linking python class to DB tables
