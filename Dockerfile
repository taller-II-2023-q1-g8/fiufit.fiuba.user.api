FROM python:3.11.2-slim-buster
WORKDIR D:\repos\Taller2\template

RUN pip install fastapi==0.95.0
RUN pip install uvicorn==0.20.0
RUN pip install fastapi sqlalchemy uvicorn psycopg2-binary

COPY . .

CMD ["uvicorn", "main:app", "--reload"]

