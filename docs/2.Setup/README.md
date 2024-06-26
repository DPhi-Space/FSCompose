# Setup

As the FSCompose software suite uses Docker Engine for the containarized applications, we need to install Docker and Docker Compose. The following guide will help you install the necessary dependencies for your OS. Start by cloning the FSCompose repository and then follow the guide for your OS.

```bash 
   git clone https://github.com/DPhi-Space/FSCompose.git
   cd FSCompose
```


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
./run.sh
```

> ⚠️ Again, check for execution permissions on it. If you get a *Permission denied* or *Command not found* error, run the following: 
>```bash
> sudo chmod +x run.sh
> ``` 

This will launch the Flight Software (FS) suite, which we will interface through tcp with a Python script (_main.py_). We will get into this in the [SECTION](TODO)

## Next Step

Now the next step is to learn how to use the GDS GUI : 

[Ground Data Segment guide](./gds.md)