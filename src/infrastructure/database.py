"""Database Connection"""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@users-db/db"
SQLALCHEMY_DATABASE_URL = environ.get("DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://users_xihj_user:pDcOCsNjoPaOfTAnd7FUG0YlMqGvY4Mp@dpg-cgsp9f1jvhtrd270hlh0-a.oregon-postgres.render.com/users_xihj"

try:
    if environ.get("DATABASE_URL") is not None:
        SQLALCHEMY_DATABASE_URL = environ.get("DATABASE_URL")
        print("DATABASE_URL Found in Environment:", SQLALCHEMY_DATABASE_URL)
    else:
        print("DATABASE_URL Found in Environment is None")
except KeyError:
    print("DATABASE_URL NOT Found in Environment, using local url")


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
