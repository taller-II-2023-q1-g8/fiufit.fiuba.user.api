"""Database Connection"""

from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres/db"

try:
    if environ.get("DATABASE_URL") is not None:
        SQLALCHEMY_DATABASE_URL = environ.get("DATABASE_URL")
        print("DATABASE_URL Found in Environment:", SQLALCHEMY_DATABASE_URL)
    else:
        print("DATABASE_URL Found in Environment is None")
except KeyError:
    print("DATABASE_URL NOT Found in Environment, using local url")


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
