#!/bin/bash

FILE=nitro-enclave-python-demo.eif
if [ -f "$FILE" ]; then
    rm $FILE
fi
docker rmi -f $(docker images -a -q)
nitro-cli run-enclave --cpu-count 2 --memory 2048 --eif-path nitro-enclave-python-demo.eif --debug-mode
nitro-cli console --enclave-id $(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
docker build -t nitro-enclave-python-demo:latest .
nitro-cli build-enclave --docker-dir ./ --docker-uri nitro-enclave-python-demo:latest --output-file "$FILE"
