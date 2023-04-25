[![codecov](https://codecov.io/gh/taller-II-2023-q1-g8/TemplateFastAPI/branch/master/graph/badge.svg?token=CM3FJKHBQ0)](https://codecov.io/gh/taller-II-2023-q1-g8/TemplateFastAPI)
[![Pylint](https://github.com/taller-II-2023-q1-g8/TemplateFastAPI/actions/workflows/pylint.yml/badge.svg)](https://github.com/taller-II-2023-q1-g8/TemplateFastAPI/actions/workflows/pylint.yml)
# Instrucciones
Con el directorio "template" como CWD:
> docker-compose up --build

## Endpoints Implementados:
- **GET**: localhost:8000/user/
- **GET**: localhost:8000/user/?username=
- **GET**: localhost:8000/user/?email=
- **GET**: localhost:8000/user/usernames
- **GET**: localhost:8000/user/usernames?prefix=
- **PUT**: localhost:8000/user
- **DELETE**: localhost:8000/user/{user_id}
- **POST**: localhost:8000/user

## Requisitos:
- Docker
