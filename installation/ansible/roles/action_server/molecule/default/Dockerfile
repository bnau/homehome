FROM ubuntu:22.04

RUN apt-get update && apt-get install -y init systemd systemd-sysv sudo && apt-get clean all
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo