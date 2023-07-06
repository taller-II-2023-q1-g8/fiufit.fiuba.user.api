"""Database Connection"""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = environ.get("DATABASE_URL")

engine = None
SessionLocal = None
Base =  declarative_base()

try:
    if environ.get("DATABASE_URL") is not None:
        SQLALCHEMY_DATABASE_URL = environ.get("DATABASE_URL")
        print("DATABASE_URL Found in Environment:", SQLALCHEMY_DATABASE_URL)
        engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=10)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    else:
        print("DATABASE_URL Found in Environment is None")
except KeyError:
    print("DATABASE_URL NOT Found in Environment, using local url")
