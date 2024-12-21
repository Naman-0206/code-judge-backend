# FROM ubuntu:22.04

# RUN apt-get update && \
# apt-get install -y iputils-ping && \
# apt-get install -y python3-pip g++ && \
# apt-get clean && \
# rm -rf /var/lib/apt/lists/*

FROM my-ubuntu-image

WORKDIR /worker

COPY . /worker/submission_worker

RUN pip3 install -r submission_worker/requirements.txt

CMD ["python3","-u", "-m", "submission_worker.rabbitmq"]