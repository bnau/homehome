FROM ubuntu:18.04

ENV DEBIAN_FRONTEND snoninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update
RUN apt-get install -y gcc python-dev libkrb5-dev
RUN apt-get install python3-pip -y
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade virtualenv
RUN pip3 install pywinrm[kerberos]
RUN apt install krb5-user -y
RUN pip3 install pywinrm
RUN pip3 install ansible
