# Commands

## Time of Execution

All commands except for *downlink* need to add a time of execution prefix to the command. It can be either relative to the previous command or absolute timing. Both types are explained below :

### Absolute Execution Time
The Absolute Execution Time executes commands at the given absolute calendar time. It's Prefix has the following format, an ‘A’ followed by ISO_8601 ordinal datetime format with optional subseconds:

```
AYYYY-DDDTHH:MM:SS[.sss] [command]
```

Where:

- **A** indicates it is a relative timed command

- **YYYY** sets the year 

- **DDD** sets the day of the year

- **HH** sets the hour

- **MM** sets the minutes

- **SS** sets the seconds


The example below will execute the command the 20th of August of 2024, at 15h02 and 1 second: 

```
A2024-232T15:02:01 [command]
```

On Linux, you can easily fetch the day of the year of a given date with the following command : 

```
$ date --date="2023-07-25" +%j
206
```


Which gives you the *DDD* argument of the Prefix, 206 in this example.

### Relative Execution Time
The Relative Execution Time is relative to the previous command's execution time and it's Prefix has the following format : 

```
RHH:MM:SS [command]
```

Where:

- **R** indicates it is a relative timed command

- **HH** sets the relative hour

- **MM** sets the relative minutes

- **SS** sets the relative seconds

If the first command in a command sequence is Relative Execution timed, it will execute relative to the start of the command sequence.


```
R00:00:02 build Dockerfile.integration integration-img
```

**Note** Relative times cannot exceed 24 hours for now.



## Commands
### *[time] build [Dockerfile.name] [image_tag]*

*Description*

Build a Docker Container on the Flight Software (FS).

*Parameters*
- **time** (time prefix): The time when to execute this command.
- **Dockerfile.name** (string): The name of the Dockerfile to build. Analogous to Dockers' *-f* flag.
- **image_tag** (string): The name of the built Docker Image. Analogous to Dockers' *-t* flag.

*Usage*

The first build will be executed the 21th of August 2024, at 23h02, build the Dockerfile *Dockerfile.integration* and tag the built Docker Image to  *integration-img*.

The second build command will be executed 2h32 after the previous command, *i.e.* the 22th of August 2024, at 1h02 minutes and 32 seconds. It will build the same Dockerfile, and tag the built Docker Image to *integration-img-2*

```bash
    A2024-232T23:02:00 build Dockerfile.integration integration-img
    R02:00:32 build Dockerfile.integration integration-img-2
```

### *[time] start [image_tag] [container_name]*

*Description*

Starts a Docker Container from the specified Docker Image. The Docker Image needs to be built before running this command for it to succeed.


*Parameters*
- **time** (time prefix): The time when to execute this command.
- **image_tag** (string): The name of the built Docker Image. Analogous to Dockers' *-t* flag.
- **container_name** (string): The name that will be attributed to the Docker Container. Analogous to Dockers' *--name* flag.

*Usage*

The first build will be executed the 14th of September 2024, at 15h02, build the Dockerfile *Dockerfile.integration* and tag the built Docker Image to  *integration-img*.

The second command will be executed 10 minutes and 21 seconds after the previous command, *i.e.* the 14th of September 2024, at 15h12 and 21 seconds. It will start the Docker Container from the previously built *integration-img* Docker Image, and name this Docker Container *testing-interface*

```bash
    A2024-257T15:02:00 build Dockerfile.integration integration-img
    R00:10:21 start integration-img testing-interface
```



### *[time] stop  [container_name]*

*Description*

Stops a running Docker Container.

*Parameters*
- **time** (time prefix): The time when to execute this command.
- **container_name** (string): The name of the running Docker Container to be stopped. 

*Usage*

The first command will be executed immediately when the command sequence start. It will start a Docker Container from a previously built Docker Image *integration-img*, and name the Docker Container *quick-test*

The second command will be executed 21 seconds after the previous one. It will stop the previously started Docker Container. 
```bash
    R00:00:00 start integration-img quick-test
    R00:00:21 stop  quick-test
```



### *downlink  [file]*

*Description*

Requests the FS to downlink a file that is contained in the **data/** folder of the Users' volume.

*Parameters*
- **file** (string): The name of the file to be downlinked. 

*Usage*

The command will be executed immediately. It will request the FS to add the *test.txt* file to the zip file that will be downlinked to the FS Interface.

```bash
    downlink test.txt
```
**Note** The downlink command does not take a time of execution prefix.




## Full Example

Below is presented a full example of Command Sequence, in which we do the following : 

1. Build the *Dockerfile.integration* file and name the resulting Docker Image to *integration-image*.
2. Start a Docker Container from the previously built Docker Image *integration-image*, and name this Docker Container to *run-integration*
3. Stop the running Docker Container named *run-integration*
4. Request downlink of the log.txt, which is foun in the **data/** folder of the users volume in the FS.


```
R00:00:00 build Dockerfile.integration integration-image

R00:00:10 start integration-image run-integration

R00:00:30 stop run-integration

downlink log.txt

```