# build the docker container
docker build -f Dockerfile.integration -t integration-test --load . 

# run the docker container
docker run --device /dev/ttyACM0 integration-test