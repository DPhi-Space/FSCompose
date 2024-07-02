#!/bin/bash

create(){
    docker service create \
        --name registry \
        --publish 5000:5000 \
        --network $CG_NETWORK \
        registry:2 
    while [ "$(docker service ls --filter name=registry -q)" = "" ]; do
        echo "Waiting for registry service to be created..."
        sleep 5
    done
    echo "Registry service created."
}

remove(){
    echo "Removing Registry"
}

fill(){
    ./deploy/volume-creator.sh create
    ./deploy/registry-filler.sh --hostname $hostname
    echo "Register filled"
}

if [ "$1" = "create" ]; then
    create
elif [ "$1" = "remove" ]; then
    remove
elif [ "$1" = "fill" ]; then
    fill
else
    echo "Usage: $0 {create|remove}"
fi