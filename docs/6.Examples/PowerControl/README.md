# Example: Power Control

In this example we will be going through the development and deployment of a Docker Container that posts power requests to the Flight Software, so that a specific port in the payload's dedicated power channel can be turned on and off. 

If you have not already cloned the repo, do so by running the following:

```bash
$ git clone git@github.com:DPhi-Space/FSCompose.git
$ cd FSCompose/
$ python3 -m venv venv 
$ . venv/bin/activate
$ pip install -r requirements.txt
```


## First Step: Local Development

### Docker overview

We will be running the simple `payload.py` shown below. It uses the provided `pdb_fun.yp` to post power requests to the FS. When testing locally, we will be using a stub of the `pdb_fun.py`, as there is no FS running to connect to. The script below simply turns on and off the payload every 30 seconds, and requests the power state of the given port:

```python
# payload.py
import time
from pdb_fun import PowerControl

if __name__ == "__main__":

    power = PowerControl()
    print("PDB Control Example")
    
    while True:
        power.set_power(0, True)
        print("Current power state port 0: ", power.get_power(0))
        time.sleep(30)
        power.set_power(0, False)
        print("Current power state port 0: ", power.get_power(0))
        time.sleep(30)
```

We can verify it correctly runs naked, *i.e.* outside a Docker Container, by running :

```bash
$ python3 power.py
> PDB Control Example
> Current power state port 0:  {'power': True}
> Current power state port 0:  {'power': False}
```

Then let's write a Dockerfile that includes the `payload.py` and the `pdb_fun.py` files, which is a Python wrapper for the REST API of the Power Control, provided by DPhi Space. We will also need to include the `user.json`, which is used to authenticate communications with the Power Manager on the Flight Software. Don't worry, this file will be provided to you in your Docker Volume by DPhi Space, we just need to make sure to copy it into the Docker Image we will create. For the local build this file can be empty as it is simply a stub. 



```docker
FROM python:3.9-slim

WORKDIR /app

RUN pip install requests

COPY ./pdb_fun.py /app/
COPY ./user.json /app/
COPY ./payload.py /app/

EXPOSE 80

CMD ["python3","-u", "payload.py"]
```

To make sure everything build locally, run the following command : 

```bash
$ docker build -f Dockerfile.power -t power-control .
```

And we should also verify it works locally :

```bash
$ docker run power-control
> PDB Control Example
> Current power state port 0:  {'power': True}
> Current power state port 0:  {'power': False}

```

At this point, we have locally validated that the Docker Container we want to run works. Let's integrate it in the FSCompose suite and run it inside it!

## Second Step: FSCompose Testing
### Local FS Setup
First, we need to get a local deployment of the FS running. Start by logging in to the DPhi Space Private Registry, with the credentials provided by e-mail:

```bash
$ docker login ops.dphi.space
> Username: [username] 
> Password: [password]
```

This will allow you to pull the pre-built Docker Images necessary to run the FS locally. 


### GS Setup
The Ground Segment will be the interfaces users use to communicate with the Flight Software once Clustergate is deployed in Space. Therefore, for development and testing we will be using the same software suite, to validate the development and deployment pipeline.

Head to the [GS Dashboard](http://ops.dphi.space:8000/login/) and login with your credentials. Then, go to the **Files** tab, upload the `Dockerfile.power` and the `payload.py` we created earlier and set it to *Uplink* by clicking the **Uplink** button next to the file after uploading it. 

    ❗:bangbang: :warning: **DO NOT INCLUDE** `user.json` **NOR** **pdb_fun.py**: these will be automatically added to your private Docker volume, where the Containers are built.

This should be the result: 

![alt text](./imgs/files-uplink.png)

This tells the GS that the file is to be uplinked (*i.e.* sent to the satellite or to the local deployment of the FS, which are analogous) to the FS on the next communication window. The next step is to write a Command Sequence on the **Commander** tab to tell the FS when to build the Docker Image and run the Docker Container from this built Image. Below is an example of Command Sequence:

```
R00:00:00 build_start Dockerfile.hello hello-img hello-container
R00:02:00 stop hello-container
```

For a more in detail exaplanation of the commands, check out the [Commander](../../3.GroundSegment/Commands.md) section

This should result in the following:

![alt text](./imgs/cmds.png)


Hit **Compile**, and activate the Command Sequence in the *Command Files* list, to tell the GS to prepare this Command Sequence in the next communication window with the FS, by clicking on the **Inactive** button. The result is shown below:

![alt text](./imgs/cmds-file.png)

Now everything is ready to run on the FS.

### FS-GS Interface


Now we are ready to run the FSCompose:

```python
$ cd FSCompose/
$ python3 main.py
```

Enter your GS credentials so that it correctly interface with your session. Once the local deployment of the FSCompose is ready, you will see the following output: 

```bash
Connecting to  0.0.0.0 50000
Starting FS Interface
Username: [username] 
Password: [password]
Login successful

(...)

Starting fs-interface...

Press e to execute Command Sequence
Press s to send downlink.zip to GS
Press q to quit

Waiting for Instructions 

```

Now everything is ready. Press **e** to execute the Command Sequence we wrote before for the FS to build and start the Docker Image and Container. 

This will take a minute or two. The expected output is shown below:

```
Waiting for Instructions e
{'Authorization': 'Token 28db0f69442675fc29fea3fcb3b7d44d861d30c7'}
Zip retrieved successfully
FS executing command sequence...Patience.
FS executing command sequence...Patience.
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Waiting for downlink files...
Received File  downlink.zip
Waiting for Instructions 
```

Once we correctly receive the downlink.zip from the FS on the interface script, press **s** and enter to send it to the GS for processing:
```
Received File  downlink.zip
Waiting for Instructions s
Sending zip to GS...
Zip sent successfully
Waiting for Instructions 
```

Congratulations! You have successfully controled the power channel of your payload from within your Docker Container. As usual, the output produced by the latter will be logged into a log file. Back in the GS Dashboard, we can see that new files appeared in the **On-Board Log Files** Section in the *Files* tab. Whenever a Docker Container is executed in the FS, it's standard output (*i.e.*, any *std::cout* in C++ or any *print()* in Python) will be captured and logged. Let's request their *downlink* and deactivate the Command Sequence, so that they are directly downlinked:

![alt text](./imgs/files-onboard.png)

![alt text](./imgs/cmder-deactivate.png)


Now, when we execute the Command Sequence, the file will be added to the `downlink.zip` file, which is transferred from the FS to the interface script. Wait for the same output as before:


```
Received File  downlink.zip
Waiting for Instructions s
Sending zip to GS...
Zip sent successfully
Waiting for Instructions 
```

And press **s** in the `main.py` to send it to the GS. Now, back in the GS Dashboard, we will see the requested file appear in the **Downlinked Files** Section of the *Files* tab: 

![alt text](./imgs/log-download.png)

Which we can directly download and visualize. You should see the following : 

```
2024-07-24T16:53:29+00:00	jsilveira/jsilveira-power-container	{"message":"PDB Control Example"}
2024-07-24T16:53:29+00:00	jsilveira/jsilveira-power-container	{"message":"Current power state port 0:  {'power': True}"}
2024-07-24T16:53:59+00:00	jsilveira/jsilveira-power-container	{"message":"Current power state port 0:  {'power': False}"}

```

Congratulations ! Everything worked out.

# Debug

By running the following comand:

```bash
$ ./debug.sh
```

You can copy from the FS the files in your `app/data/` folder, which is where the Dockerfiles and scripts are transferred to, and also the log files of the Docker Images and Containers the FS tries to build and to execute. This can help in case something goes wrong in the execution:

```bash
$ ./deploy.sh
Successfully copied 28.7kB to ~/FSCompose/debug/

Fetched the following files from FS:
./debug/
├── jsilveira
│   ├── Dockerfile.hello
│   ├── Dockerfile.payload1
│   ├── Dockerfile.power
│   ├── Dockerfile.serial
│   ├── log.txt
│   ├── payload.py
│   ├── pdb_fun.py
│   ├── pdb_fun.stub.py
│   ├── requirements.txt
│   ├── serial-test.py
│   └── user.json
├── logs-file-tree.log
├── power-container.log
├── power-img.log
├── providers-file-tree.log
├── unzip-logs.log
└── zip-files.log

1 directory, 17 files
``` 