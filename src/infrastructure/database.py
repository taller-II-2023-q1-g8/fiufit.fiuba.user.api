from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_user = "users_ihwj_user"
db_name = "users_ihwj"
db_pass = "g9F5EtSgbaLDIJJTIZ1aI70ZxruQNt9w"
db_host_name = "dpg-cgoqtv5269v5rjd5gl20-a"
db_port = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host_name}/{db_name}"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres/db" #For Dev Environment

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
