#!/bin/bash

docker build -t users-ms . &&
docker run -p 8000:8000 --network fiufit-network --rm --name users-ms --env-file=env-file.txt users-ms:latest
