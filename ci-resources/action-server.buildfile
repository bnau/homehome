FROM node:18

RUN apt-get update && apt-get install -y build-essential libbluetooth-dev