FROM ubuntu:22.04

ENV TZ=Europe/Warsaw
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SDKMAN_DIR="/root/.sdkman"
#zmienne srodowiskowe

RUN apt-get update && apt-get install -y vim git

# instalowanie pythona
RUN apt-get install -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.8

# instalacja javy
RUN apt-get install -y openjdk-8-jdk

# instalacja kotlina
RUN apt-get install -y curl zip unzip

# Instalacja SDKMAN! a z niego kotlin i gradle
RUN curl -s https://get.sdkman.io | bash
RUN chmod a+x "$HOME/.sdkman/bin/sdkman-init.sh"
RUN bash -c "curl -s https://get.sdkman.io | bash && source \"$SDKMAN_DIR/bin/sdkman-init.sh\" && sdk install kotlin && sdk install gradle"

RUN mkdir /app
RUN mkdir -p /app/src/main/java

COPY build.gradle /app
COPY HelloWorld.java /app/src/main/java

WORKDIR /app

CMD ["bash", "-c", "source \"$SDKMAN_DIR/bin/sdkman-init.sh\" && gradle run"]