# FROM ubuntu:22.04

# RUN apt-get update && \
#     apt-get install -y iputils-ping && \
#     apt-get install -y python3-pip g++ && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

FROM my-ubuntu-image

WORKDIR /worker

COPY . /worker/execution_worker

RUN pip3 install -r execution_worker/requirements.txt

CMD ["python3","-u", "-m", "execution_worker.rabbitmq"]