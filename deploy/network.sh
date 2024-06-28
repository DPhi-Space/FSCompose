#!/bin/bash

remove(){
    docker network rm $CG_NETWORK
    while [ "$(docker network ls --filter name=clustergate_network -q)" != "" ]; do
        echo "Waiting for orphaned network to be removed..."
        sleep 2
    done

}

create(){
    if [ $(docker network ls -q -f name=$CG_NETWORK | wc -l) -eq 0 ]
    then
        docker network create \
                --driver overlay \
                --attachable \
                --subnet "172.30.0.0/24" \
                --scope swarm \
                $CG_NETWORK

        while [ "$(docker network ls --filter name=$CG_NETWORK -q)" = "" ]; do
            echo "Waiting for network $CG_NETWORK to be created..."
            sleep 5
        done

        echo "Network $CG_NETWORK created."
    else
        echo "Network $CG_NETWORK already exists."
    fi
}


if [ "$1" = "create" ]; then
    create 
elif [ "$1" = "remove" ]; then
    remove 
else
    echo "Usage: $0 {create|remove}"
fi