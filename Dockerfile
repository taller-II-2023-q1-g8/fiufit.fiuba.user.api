FROM python:3.10.12-alpine
WORKDIR /app
COPY requirements.txt .
COPY ./main.py .
COPY ./src ./src
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
ENV DATABASE_URL=postgresql://user:password@postgres:5432/db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]