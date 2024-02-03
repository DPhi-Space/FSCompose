# Setup
## WSL v2 
Unfortunately, Docker Desktop for Windows does not support WSL v1. However, you can use Docker Desktop for Windows with WSL v2. To do so, follow the guide below:

[https://docs.docker.com/desktop/windows/wsl/](https://docs.docker.com/desktop/windows/wsl/)


## Linux 
For Linux, we provide a setup script that will take care of the necessary dependencies for you. Execute with admin privilege : 

```bash
sudo ./setup.sh
```

> ⚠️ Make sure you have execution permissions on it. If you get a *Permission denied* or *Command not found* error, run the following: 
>```bash
> sudo chmod +x setup.sh
> ``` 

# Run the FSCompose
To start the FSCompose, run the following script. 
```bash
sudo ./run.sh
```

> ⚠️ Again, check for execution permissions on it. If you get a *Permission denied* or *Command not found* error, run the following: 
>```bash
> sudo chmod +x run.sh
> ``` 


Depending on the OS and user settings, the GUI might not open automatically. If that is the case, please open: 

[127.0.0.1:5000/](http://127.0.0.1:5000/)

If you prefer to go through the process yourself, follow the steps below.

## 1 Install Docker and Docker Compose
As we want to containarize and isolate every application on board, we need Docker. First install **Docker Engine** by following the guide below:

[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

Then install the **Docker Compose** plugin by following this guide : 

[https://docs.docker.com/compose/install/linux/](https://docs.docker.com/compose/install/linux/)


> ⚠️We will be using the Docker Compose V2, as V1 is deprecated, i.e. `docker compose` without the hyphen.


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