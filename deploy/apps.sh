#!/bin/bash

create(){

    export FSW_IP=$(docker inspect -f '{{.NetworkSettings.Networks.clustergate_network.IPAddress}}' $(docker ps -q --filter "name=fsw"))
    echo "Starting PDB"
    docker pull ops.dphi.space/pdb-api
    docker service create \
        --name pdb-api \
        --network clustergate_network \
        --host fsw:$FSW_IP \
        ops.dphi.space/pdb-api:latest
}

pdb_create_users(){
    jq -c '.providers[]' ./deploy/providers.json | while read provider; do
        name=$(echo "$provider" | jq -r '.name')
        payload=$(echo "$provider" | jq -c '.payloads')
        hash=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo)
        user_json="{\"username\"  :   \"${name}\", \"password\"  :   \"${hash}\", \"payload\"  :   ${payload}}"
        echo "$user_json" > ./deploy/${name}_pdb.json

        docker cp ./deploy/${name}_pdb.json fsw:/app/payloads/${name}/user.json
        docker cp ../Apps/pdb/pdb_fun.py fsw:/app/payloads/${name}/pdb_fun.py
        echo "Created PDB Client: $user_json"
        sleep 1
    done
}

remove(){
    echo "Removing Apps"
}

if [ "$1" = "create" ]; then
    create
elif [ "$1" = "pdb_users" ]; then
    pdb_create_users
fi