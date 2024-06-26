
# Flight Software

## Setup

To start the local deployment of DPhi Space Flight Software (FS), first login to our private Docker Registry. Use the same acount one would use to login nto the DPhi Space Dashboard

```bash
$ docker login ops.dphi.space
Username: [Username]
Password: [Password]
```
Now you are ready to run the deployment script : 

```bash
$ ./run.sh
```

## Flight Software Interface

To interface between the FS and GS, we provide the `main.py` python script, which will fetch the files from the GS and send them to the FS, start the command sequence execution on the FS side and wait for the files the FS will send back. Once it receives them, it will be ready to upload these files to the GS, where the user can view and download them. 

Start by running the script and enter the same login information as for the GS: 

``` bash
$ python3 main.py
Connecting to 0.0.0.0 50000
Starting FS Interface
Username:[Username]
Password:[Password]
Login successful
Starting fs-interface...

Press e to execute Command Sequence
Press s to send downlink.zip to GS
Press q to quit

Waiting for Instructions 
```

To execute the Active Command Sequence, which is set in the *Commander* tab of the GS, press e.
Once the script receives the files back from the FS, the script will be ready to re-execute an action. Press s to send the received files to the GS so that they can be distributed and processed. The user can also directly analyse them by extracting the *downlink.zip* files.


## Data Folder

Each Docker Container started by the user will have a shared folder with the main FS mounted. The folder is mounted at `data/` inside the Docker Container, and should be used for the data that needs to be downlinked, as well as for the data that needs to be uplinked to the FS. This is the only folder shared with the FS from the Payload Docker Container, and provides a way to exchange data between two Docker Containers deployed by the same user.

All of the data a user would want to downlink from the FS needs to be moved to folder. [Here](../6.Examples/README.md) we provide examples on how to manage this data transfer.  