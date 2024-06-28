#!/bin/bash

set -e

create(){

    docker volume create logs
    docker pull ops.dphi.space/logger:latest
    
    docker service create \
        --name logger \
        --publish 24224:24224 \
        --network $CG_NETWORK \
        --mount source=logs,target=/fluentd/log \
        ops.dphi.space/logger:latest

    while [ "$(docker service ls --filter name=logger -q)" = "" ]; do
        echo "Waiting for logger service to be created..."
        sleep 5
    done

    echo "Logger service created."
}


if [ "$1" = "create" ]; then
    create
fi