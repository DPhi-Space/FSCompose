# Setup


## 1 Install Docker 
Checkout this guide 

[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

## 2 Clone the git 

   ```bash
   git clone https://github.com/DPhi-Space/FSCompose.git
   cd FSCompose
   ```



## 3 Run Docker Compose 

The Docker Compose includes the containers for the main Flight Software(FS), the Ground Data Segment(GDS) and the Payloads. When running it, it should pull the images from the Docker Hub.

   
   ```bash   
   docker compose up -d fsw gds
   ```
      
The FS will try periodically to connect to ports 50001 and 50002. Create a Python script that starts a TCP server on those ports. Example provided in `example.py`

## Next Step

Now the next step is to learn how to use the Ground Data Segment GUI : 

[GDS guide](./gds.md)