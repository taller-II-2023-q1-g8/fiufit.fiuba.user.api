FROM python:3.9.16-bullseye
WORKDIR .

RUN apt-get update
RUN apt-get -y install gcc
RUN pip install fastapi==0.95.0
RUN pip install uvicorn==0.20.0
RUN pip install sqlalchemy psycopg2-binary pytest pytest-cov
RUN pip install pyrebase

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]