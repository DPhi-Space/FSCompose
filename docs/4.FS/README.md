
# Flight Software

## Flight Software Interface

To interface between the FS and GS, the `main.py` script will start a Flight Software Interface thread, which will wait for instruction after setting up the FSCompose and fetching the necessary files from the GS Dashboard, $i.e.$, `payloads_files.zip`: 

``` bash
Starting FS Interface
Username: [Username]
Password: [Password]
Login successful
Zip retrieved successfully
Starting fs...

(...)

Setup ready!
Starting fs-interface...

Press e to execute Command Sequence
Press s to send downlink.zip to GS
Press q to quit

Waiting for Instructions Cmd seq len  136
```

- To execute the Active Command Sequence, which is set in the *Commander* tab of the GS, press **e**.
- To uplink the `downlink.zip` file received from the FSCompose after it finished executing a Command Sequence, press **s**
- To quit the FSCompose suite, press **q**. It is important to quit in this fashion, as otherwise the Containers might not stop correctly and jam the TCP ports on the next run of the whole software suite.

Once the script receives the files back from the FS, the script will be ready to re-execute an action. Press **s** to send the received files to the GS so that they can be distributed and processed. The user can also directly analyse them by extracting the `downlink.zip` files.


## Data Folder

Each Docker Container started by the user will have a shared folder with the main FS mounted. The folder is mounted at `data/` inside the Docker Container, and should be used for the data that needs to be downlinked, as well as for the data that needs to be uplinked to the FS. This is the only folder shared with the FS from the Payload Docker Container, and provides a way to exchange data between two Docker Containers deployed by the same user.

All of the data a user would want to downlink from the FS needs to be moved to folder. [Here](../6.Examples/README.md) we provide examples on how to manage this data transfer.  


