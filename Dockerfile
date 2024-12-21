FROM ubuntu:22.04

RUN apt-get update && \
apt-get install -y iputils-ping && \
apt-get install -y python3-pip g++ && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*