#!/bin/bash

docker run --network fiufit-network -p 5432:5432 --volume users-db:/data --rm --name users-db --env-file=db-env-file.txt postgres
