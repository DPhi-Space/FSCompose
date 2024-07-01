#!/bin/bash
mkdir -p debug/
docker cp fsw:app/payloads/. ./debug/
echo
echo "Fetched the following files from FS:"
tree ./debug/