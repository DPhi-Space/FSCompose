![](leds.gif)
# Arduino Nano Control

## Introduction 
In this example, we will be controlling an Arduino Nano from within the FSCompose software suite. The payload setup is quite simple, as shown below.

![](nano.jpeg)

The Arduino is quite a simple subsystem in this example. It receives messages of 1 byte and executes a LED pattern according to the byte received. It has a total of 7 patterns. The code can be found under `payload-example/arduino-nano/`.

The Arduino communicates through serial with the python script. We will go through the three expected stages of development : 
1. Direct interfacing with the script running on the PC.
2. Containarized interfacing, where the script runs inside a docker container.
3. FSCompose interfacing, where the previous docker container is uploaded to the FSCompose, built and then ran from the GDS GUI.

Let's get started.

## Direct Interfacing

The python script is as follows :

```python
import serial
import time 

ser = serial.Serial("/dev/ttyACM0", 115200)
packet = bytearray()

for i in range(0x00, 0x07):
    packet.append(i)
    ser.write(packet)
    time.sleep(5)
```

It is the standard python way to interface with a serial device. Almost a direct copy-paste of what you can find on Stackoverflow. Which will come in handy, as developers we want to fly as we develop and develop as we fly. No need to adapt to an SDK. No need to adapt to an API. No need to adapt to the hardware. 

>⚠️ Before running the script make sure to correctly configure the serial port. 

Now run the script and enjoy the LED show: 

```bash
python3 payload-nano.py
```

>⚠️ Make sure you have the necessary permissions to access the serial port. If when running the script you get the following error : 
> ```bash
>   OSError: [Errno 13] Permission denied: '/dev/ttyACM0'
>```
> Then run the following command : 
> ```bash
>   sudo chmod +666 /dev/ttyACM0
>```


## Containarized Interfacing
Now, we want to containarize this application. This encapsulates the application and adds to general reliability of it. The Dockerfile we'll be using is quite simple : 

```docker
ARG VARIANT="22.04"
FROM ubuntu:${VARIANT} as base

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-setuptools \
    python3-pip 

RUN pip install pyserial

COPY    ./payload-nano.py ./payload.py

CMD   python3 -u payload.py 
```

Inside the folder containing both the script and the dockerfile (in our case `/payload-example/arduino-nano/`), run the following in the terminal to build the image: 

```bash
$ docker build -f Dockerfile.nano -t nano .
```

And after it successfully builds, we can run it by executing the following in the terminal : 

```bash
$ docker run nano
```

This will raise an error in the python, as we have not exposed the serial device to the container for it to interface with the arduino. The correct command is : 

```bash
$ docker run --device /dev/ttyACM0 nano
```

>⚠️ Once again, make sure the serial device you are exposing to the container is the correct one. 

Let's say in the python script we set the serial device to be `/dev/ttyACM0`, but the serial device in the PC keeps changing for whatever reason. We can map it to always be `/dev/ttyACM0` inside the container by running 

```bash
$ docker run --device /dev/ttyUSB0:/dev/ttyACM0 nano
```

Where `/dev/ttyUSB0` is the serial device in the PC. This might be different for you of course.

Now run the docker container and, again, enjoy the light show.



## FSCompose Interfacing

Now the FSCompose suite. Follow the [setup](../../setup.md) setup guide if not already done to get started with installation and setup. Let's start by launching the FSCompose suite : 

```bash 
$ docker compose up -d fsw gds
```

This will launch the core Flight Software (FS) and the GDS GUI to interface with it at the following address : 

http://127.0.0.1:5000/


Open it on your browser of choice. Let's upload the files we need to build the docker image for our payload. Go to the **Uplink** Tab and select the `payload-nano.py` script and the `Dockerfile.nano` and set the *Destination folder* to `/app/payload`, as shown below:

![](image.png)


Uplink the files by pressing on the orange *Uplink* button. You can verify the correct uplink in the **Events** Tab, which should show the following events: 

![](image-1.png)


Now we are almost ready to build it. One last detail, we need to update the compose file to include this new service. Remember, it is the **fsw** container that will manage your payload container, and it has an internal copy of the `docker-compose.yml` file, which needs to be updated to include the new payload. All of this will be automated when your payload is in space, but for testing and development freedom reasons, we leave this up to the developers during the development phase. Let's append the following code to the `docker-compose.yml` file : 

```docker
  payload-nano:
    image: nano:latest
    volumes:
      - payload:/app/data
      - sharepoint:/app/sharepoint
    networks:
      my_network:
        ipv4_address: 172.30.0.10
    devices:
      - "/dev/ttyACM0:/dev/ttyACM0"           
```

The caveats are the following: 
- `payload-nano` this is the name of the service. It is used as an argument for the *dockerManager.Start* and *dockerManager.Stop* commands.
- `image: nano:latest` this is the name of the image this service should search for. This must coincide with the second argument of the *dockerManager.BuildPayload* command, which sets the name of the container being built.
- `volumes:` sets up the shared volumes with the core flight software and other containers if they wish to share data.
- `network:` sets up the IP address of this service within the local network docker creates.
- `devices:` this is probably the most important setting, as it exposes the serial device of the host computer running the whole docker compose suite to this specific service. Meaning that, if you have an arduino connected to `/dev/ttyACM0` in the host computer, you can forward that port to this service by defining and rename it to `/dev/ttyUSB0`(so you don't have to adapt the port's name inside the service). 

Now we will uplink the file to the `/app` folder, as such: 

![Alt text](image-2.png)

Let's build the payload inside the **fsw** now. Go to the **Commanding** Tab and send the *dockerManager.BuildPayload* command with the arguments shown below:

![Alt text](image-4.png)

The first argument is the name of the docker file we uploaded, in our case it is `Dockerfile.nano`. The second argument is the name of the container, as we have defined in the `docker-compose.yml`. 
If the build has succeded, we are ready to start the container. Send the *dockerManager.Start* command with the following argument: 

![](image-5.png)

🎉🥳🛰️

This time, enjoy both the LED show and successfully finishing the necessary integration, software-wise, to fly with DPhi Space!

🎉🥳🛰️



