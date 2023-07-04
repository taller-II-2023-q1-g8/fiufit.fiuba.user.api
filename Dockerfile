####### First Time ############
# FROM python:3.9.16-bullseye
# WORKDIR /app

# RUN apt-get update
# RUN apt-get -y install gcc

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY src ./src
# COPY main.py .

####### Upgraded First Time ############
FROM python:3.10.12-alpine
WORKDIR /app
COPY requirements.txt .
COPY ./main.py .
COPY ./src ./src
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt



####### Fast Build ############

# FROM users-ms:latest
# WORKDIR /app
# COPY ./main.py .
# COPY ./src ./src
# COPY ./fiufit-73a11.json .



# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]