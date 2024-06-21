#!/bin/bash

generate_volume_mounts() {
    echo "--mount type=volume,source=volume_automaton,target=/app/constraints "
    cat ./deploy/providers.json | jq -r '.providers[].name' | while read provider; do
        volume_name="volume_${provider}"
        echo "--mount type=volume,source=$volume_name,target=/app/payloads/$provider "
    done
}


create_volumes() {
    echo "Creating Volumes"
    cat ./deploy/providers.json | jq -r '.providers[].name' | while read provider; do
        volume_name="volume_${provider}"
        docker volume create $volume_name
    done
    sleep 2    
}

if [ "$1" = "create" ]; then
    create_volumes
elif [ "$1" = "generate" ]; then
    generate_volume_mounts
else
    echo "Usage: $0 {create|destroy}"
fi