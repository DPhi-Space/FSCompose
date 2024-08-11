# Setup

As the Flight Software Compose (FSCompose) suite uses Docker Engine for the containarized applications, we need to install Docker and Docker Compose. The following guide will help you install the necessary dependencies for your OS. Start by cloning the FSCompose repository and then follow the guide for your OS.

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

> ⚠️ Make sure you have execution permissions on it. If you get a _Permission denied_ or _Command not found_ error, run the following:
>
> ```bash
> sudo chmod +x setup.sh
> ```

# Run the FSCompose

To kick-off development, start by creating a new python environment and installing the necessary packages to run the local:

```python
    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip3 install -r requirements.txt
```

Before starting the FSCompose, the user needs to enter the following information into **deploy/providers.json** configuration file:

- **name**: this needs to match the login username for the GS Dashboard.
- **devices**: this will be the device attached to the Docker Containers the user will be managing with FSCompose. It allows the Docker Container to communicate with the outside world on the given device. It can be empty.
- **payloads**: name of the payload.

Below is an example on how to fill it up:

```json
{
  "providers": [
    {
      "name": "DiamondDogs",
      "devices": ["/dev/ttyACM0"],
      "payloads": ["ArduinoMega"]
    }
  ]
}
```

To start the local deployment of DPhi Space Flight Software (FS), first login to our private Docker Registry. Use the login credentials provided by email for the Docker Registry:

```bash
$ docker login ops.dphi.space
Username: [Username]
Password: [Password]
```

Now we are ready to start the FSCompose, run the following script.

```bash
$ python3 main.py
```

It will request for your GS Dashboard login credentials, which are used to fetch the files you have uploaded to it. Once the credentials are validated, it will fetch the `payloads_files.zip`, pull the Docker Containers of the FSCompose from the private Docker registry, launch the FSCompose suite, and then start the FS Interface software to communicate with the FSCompose. We will get into the latter in the [Flight Software](../4.FS/README.md) section.

## Next Step

Now the next step is to learn how to use the Ground Segment:

[Ground Segment](../3.GroundSegment/README.md)
