# Introduction
The FSCompose is a software suite that allows any payload provider, user or even a hobbyist to test and develop their payload the same way it would and will be deployed in space when flying with DPhi Space. Software-wise, the architecture is as shown in the image below. Here we will describe how to use this software suite during development and testing of the payload on the ground. 

![](imgs/architecture.jpg)

The main components of the system are : 

 - **Browser GUI** The user interacts with the system through the Ground Data Segment GUI, which is launched on the web browser. Through it, commands can be sent and telemetry downlinked to and from the Core DPhi Software. 
 - **Core DPhi Software** The main software managing and overseeing the payloads runs on DPhi's On-Board Computer. For testing purposes, a Docker container encapsulates the exact same software as the one in the flight model. Therefore, from a software and data point of view, running the FSCompose with this container is analogous to flying for the payloads. 
 - **Hardware Controller**
 - **Software Payload**
 - **Hardware Payload**



 