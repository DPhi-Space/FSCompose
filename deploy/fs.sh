#!/bin/bash

create(){
    #docker pull ops.dphi.space/gds:latest

    #docker service create \
    #--name gds \
    #--publish $GDS_PORT:5000 \
    #--log-driver=fluentd \
    #        --log-opt fluentd-address=localhost:24224 \
    #        --log-opt tag="gds" \
    #--network clustergate_network \
    #ops.dphi.space/gds:latest

#    gds_ip=$(docker inspect --format json -f '{{json .Endpoint.VirtualIPs}}' $(docker service ls -q --filter "name=gds") | jq -r '.[1].Addr' | cut -d '/' -f1)
#    echo "Connecting to $gds_ip (GDS)"


    docker pull ops.dphi.space/fsw:latest
    
    #docker run \
    #    -e GDS_IP=$gds_ip \
    #    --name fsw \
    #    --rm --privileged --network clustergate_network  \
    #    --log-driver=fluentd \
    #        --log-opt fluentd-address=localhost:24224 \
    #        --log-opt tag="fsw" \
    #    --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
    #    --mount type=volume,source=logs,target=/app/logs \
    #    $(./deploy/volume-creator.sh generate | tr -d '\n') ops.dphi.space/fsw:latest > /dev/null &

    docker run \
    -e GDS_IP=0.0.0.0 \
    --name fsw \
    --publish 0.0.0.0:50000:50000 \
    --rm --privileged --network clustergate_network  \
    --log-driver=fluentd \
        --log-opt fluentd-address=localhost:24224 \
        --log-opt tag="fsw" \
    --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
    --mount type=volume,source=logs,target=/app/logs \
    $(./deploy/volume-creator.sh generate | tr -d '\n') ops.dphi.space/fsw:latest > /dev/null &
    sleep 3
    docker cp deploy/providers.json fsw:/app/providers.json
    
    
    export FSW_IP=$(docker inspect -f '{{.NetworkSettings.Networks.clustergate_network.IPAddress}}' $(docker $SSH_PREFIX ps -q --filter "name=fsw"))
    echo "FSW is running ($FSW_IP)"    
    
}


if [ "$1" = "create" ]; then
    create
fi