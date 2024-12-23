FROM ubuntu:22.04

RUN apt-get update && \
apt-get install -y python3-pip && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

WORKDIR /server

COPY . /server

RUN pip3 install -r requirements.txt

CMD ["python3","-u", "main.py"]