FROM python:3.11.2-slim-buster
WORKDIR .

RUN pip install fastapi==0.95.0
RUN pip install uvicorn==0.20.0
RUN pip install sqlalchemy psycopg2-binary pytest pytest-cov

COPY . .

CMD ["uvicorn", "main:app", "--reload"]

