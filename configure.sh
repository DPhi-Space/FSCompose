#!/bin/bash

# Request sudo permissions at the beginning
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit
fi

echo "Setting up daemon.json for Docker"
cp ./docker-daemon.json /etc/docker/daemon.json
systemctl restart docker.service

echo "Setting up registry hostname"

# Check if "0.0.0.0 registry" already exists in /etc/hosts
if ! grep -q "^0.0.0.0[[:space:]]\+registry" /etc/hosts; then
  echo "0.0.0.0    registry" | tee -a /etc/hosts > /dev/null
  echo "Added '0.0.0.0 registry' to /etc/hosts"
else
  echo "'0.0.0.0 registry' already exists in /etc/hosts"
fi
