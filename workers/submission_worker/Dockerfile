# FROM ubuntu:22.04

# RUN apt-get update && \
# apt-get install -y iputils-ping && \
# apt-get install -y python3-pip g++ && \
# apt-get clean && \
# rm -rf /var/lib/apt/lists/*

FROM my-ubuntu-image

WORKDIR /worker
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . /worker/submission_worker


CMD ["python3","-u", "-m", "submission_worker.rabbitmq"]