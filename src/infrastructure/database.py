from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_user = "fiufit_users_database_user"
db_name = "fiufit_users_database"
db_pass = "L7SPqYoLl81hA1Rw2EB618aTkZRtZenw"
db_host_name = "dpg-cgmspsaut4meq5kthje0-a"
db_port = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host_name}/{db_name}"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres/db" #For Dev Environment

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()