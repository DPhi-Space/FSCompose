# Use a base image with AdoptOpenJDK and install Scala and SBT
FROM adoptopenjdk:11-jdk-hotspot as base

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl 

# Install Scala
ENV SCALA_VERSION 2.13.8
RUN curl -fsSL "https://downloads.lightbend.com/scala/$SCALA_VERSION/scala-$SCALA_VERSION.tgz" | tar xfz - -C /usr/share \
    && ln -s /usr/share/scala-$SCALA_VERSION /usr/share/scala \
    && ln -s /usr/share/scala/bin/* /usr/local/bin/

# Install SBT
ENV SBT_VERSION 1.5.5
RUN curl -fsSL "https://github.com/sbt/sbt/releases/download/v$SBT_VERSION/sbt-$SBT_VERSION.tgz" | tar xfz - -C /usr/share \
    && ln -s /usr/share/sbt/bin/* /usr/local/bin/

# Install jSerialComm library
COPY build.sbt ./
RUN sbt update

# Copy only the build.sbt file to cache dependencies
COPY project/build.properties ./project/build.properties

# Copy the source code and resources
COPY . .

# Compile the Scala code
RUN sbt compile

# Build a small runtime image
FROM adoptopenjdk:11-jre-hotspot as runtime

# Set the working directory in the container
WORKDIR /app

# Copy the compiled artifacts from the base image
COPY --from=base /app/target/scala-2.13/SerialWrite-assembly-1.0.jar ./SerialWrite.jar

# Run the Scala program
CMD ["java", "-jar", "SerialWrite.jar"]
