# Setup


## 1 Install Docker and Docker Compose
As we want to containarize and isolate every application on board, we need Docker. First install **Docker Engine** by following the guide below:

[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

Then install the **Docker Compose** plugin by following this guide : 

[https://docs.docker.com/compose/install/linux/](https://docs.docker.com/compose/install/linux/)


⚠️We will be using the Docker Compose V2, as V1 is deprecated, i.e. `docker compose` without the hyphen.⚠️


## 2 Clone the git 
   Next step is to clone the FSCompose repository, which contains the Docker Compose file we need to launch the core Flight Software and the GDS. It also contains a `payload-example/` with different examples for you to get started.

   ```bash
   git clone https://github.com/DPhi-Space/FSCompose.git
   cd FSCompose
   ```


## 3 Run Docker Compose 

The Docker Compose includes the containers for the core Flight Software(FS), the Ground Data Segment(GDS) and the Payloads. 

First, pull the necessary services(the FS and the GDS containers) from Docker Hub by running : 


   ```bash
   docker compose pull fsw gds
   ```
Now we are ready to run it. We will first start the FS and the GDS containers:
   
   ```bash   
   docker compose up -d fsw gds
   ```
      
- **fsw** is the FS container. It will connect through TCP to the GDS.

- **gds** is the GDS container. It will connect through TCP to the FS and start a GUI for you to interface with the FS by sending commands and diagnosting the telemetry. 

## Next Step

Now the next step is to learn how to use the Ground Data Segment GUI : 

[GDS guide](./gds.md)