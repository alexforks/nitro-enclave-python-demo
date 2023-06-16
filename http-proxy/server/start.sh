#!/bin/env bash

FILE=nitro-enclave-python-demo.eif
nitro-cli run-enclave --cpu-count 1 --memory 2048 --eif-path "$FILE" --debug-mode
nitro-cli console --enclave-id $(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
