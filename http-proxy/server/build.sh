#!/bin/env bash

FILE=nitro-enclave-python-demo.eif
if [ -f "$FILE" ]; then
    rm $FILE
fi
docker rmi -f $(docker images -a -q)
docker build -t nitro-enclave-python-demo:latest .
nitro-cli build-enclave --docker-dir ./ --docker-uri nitro-enclave-python-demo:latest --output-file "$FILE"
bash start.sh
