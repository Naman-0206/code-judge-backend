FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3-pip g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /worker

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . /worker/submission_worker

CMD ["python3", "-m", "submission_worker.main"]
