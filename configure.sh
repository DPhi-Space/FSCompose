echo "Setting up daemon.json for docker"
cp ./deploy/docker-daemon.json /etc/docker/daemon.json
systemctl restart docker.service
echo "Setting up registry hostname"
echo "0.0.0.0    registry" | sudo tee -a /etc/hosts > /dev/null