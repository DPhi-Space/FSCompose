# Ground Data Segment GUI

Once the setup is done and the FSCompose is launched, we are ready to interface with the core Flight Software (FS). The Ground Data Segment (GDS) GUI allows you to send commands to the FS and diagnostic it's status through telemetry reports and log downlink. The GDS is a web application that can be accessed, after starting the FSCompose, at :

[127.0.0.1:5000/](http://127.0.0.1:5000/)


> ⚠️ Please ensure no other service is using this port. You can verify this by running : 

- **Windows**: Run the following then kill the process in the Task Manager with the given PID.
```bash
Get-NetTCPConnection -LocalPort 5000
```

- **Unix**
```bash
sudo netstat -tulpn | grep :5000
```

## Data Folder

The payload defined in the Docker Compose will have a shared folder with the main FS container. The folder is mounted at `data/` inside the Payload container, and should be used for the data that needs to be downlinked. 

## Sharepoint Folder

This folder is used to share files between Payload Containers. It is mounted at `sharepoint/` inside the Payload container.  

## Uplink Files from GDS to Data Folder
Before we can start our Payload Container, we need to uplink the following to the FS: 

- The Dockerfile to build the Payload Container
- The necessary files to be used by the Payload Container, such as scripts, configuration files, etc.

This is done through the GDS. Once this is done, we can build the Container on the fly and start it. 


To uplink files from the GDS to the data folder of your payload, first we need to transfer the file to the FS, and then access it through the Payload Docker Container: 

### Uplink to the Core Software
First we upload the file to the FS. Go to the **Uplink** Tab and and type the following destination path:

   ```bash
   /app/payload/
   ```
   
Then select the file you want to uplink and click on the **Uplink** button. This will Uplink this file to the `data/` folder inside the Payload Container.


![Alt text](imgs/uplink-image.png)


> ⚠️ To verify the uplink was successful, check the **Events** Tab:

![Alt text](imgs/uplink.png)



## Build a new Docker Container on the fly
Now that we have everything we need on board, it is time to build the Docker Container for your Payload. To do so, go to the **Commanding** Tab and select the **dockerManager.BuildPayload** command as shown below:

   ![Alt text](imgs/build-payload.png)

With the arguments above, this will execute the following bash command:

   ```bash
   docker build -f Dockerfile.payload1 -t payloadserial:latest .
   ```

It will build the Docker Container using the `Dockerfile.payload1` file. The `-f` flag indicates the Dockerfile name, which needs to coincide with the one we uplinked in the previous step. The `-t` flag tags the image with the name `payloadserial:latest`. 

This might take sometime, depending on the size of the Container being built. You can check the correct execution of this command on the **Events** Tab once it's done. A build log will be created with the output of the command above. In this example it is named `payloadserial_build.log` and can be found under the `app/` folder in the **fsw** container. The log's name is the same as the tag of the image plus `_build.log`, so if you change the tag, the log's name will also change.

>⚠️ You can verify the correct execution of the command in the **Events** tab: 

![Alt text](imgs/build-success.png)

>⚠️  If it fails, follow the steps in the **Check Logs** Section to downlink the docker build log.

## Update the Docker Compose and Uplink it 

Last step before we can start the Payload Container. We need to add the service to the `docker-compose.yml` file. As this is payload and setup dependent, each payload service definition might be different. We provide a template that you can modify as you see fit : 

>⚠️ This step is a hotfix and will be automated in the future. Payload Providers won't need to do this in the future.  

```yaml

  payload:
    image: payloadserial:latest
    volumes:
      - payload:/app/data
      - sharepoint:/app/sharepoint
    networks:
      my_network:
        ipv4_address: 172.30.0.10
    devices:
      - "/dev/ttyACM0:/dev/ttyUSB0"           
               
```
The different configurations are : 

- `payload:` this is the service name, which you will as an argument in the GDS GUI to start and stop the container.
- `image: payloadserial:latest` this is the container image that should be run when starting this service. This is set when you build the container, after sending the `dockerManager.BuildPayload` command (previous step).
- `volumes:` this defines the (persistant) shared previously mentionned. Do not remove them, but you can add extra ones if needed.
- `networks:` defines the IP address of this service in the docker network. You can modify it if needed.
- `devices:` this is probably the most important setting, as it exposes the serial device of the host computer running the whole docker compose suite to this specific service. Meaning that, if you have an arduino connected to `/dev/ttyACM0` in the host computer, you can forward that port to this service by defining and rename it to `/dev/ttyUSB0`(so you don't have to adapt the port's name inside the service, script or executable). 

Once you finish configuring this, uplink the `docker-compose.yml` file to the `/app` folder in the FS as shown below:

![Alt text](imgs/docker-compose.png)

Now you are ready to start the Payload Container.

## Start and Stop the Payload Container

To start a payload container, which is defined in the Docker Compose, go to the **Commanding** Tab and select the **dockerManager.Start** command.


> ⚠️ The **service name** needs to match the name of the service defined on the Docker Compose as mentionned in the previous step. In the example given before, we would run the command with the argument `payload`, as shown below:

> ![Alt text](imgs/payload-start.png)


Press the **SendCommand** button and the Payload Container will be started. You can correctly verify that it ran by checking the **Events** Tab as shown below:

![Alt text](imgs/start-success.png)
If it fails, you will see the following Event:

![Alt text](imgs/fail-event.png)


>⚠️ To examine the logs and find out why it failed, follow the **Check Logs** Section below.



Press the **StopCommand** button to stop the Payload Container.


## Downlink Files from Data Folder to GDS

## Check Logs

When start or building docker containers, two log files are created : 

   

## Next Steps
[Controlling an Arduino Nano](./sections/examples/nano/ex-nano.md)


