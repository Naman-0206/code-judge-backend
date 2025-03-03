FROM ubuntu:22.04

RUN apt-get update && \
apt-get install -y python3-pip && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /server

COPY . /server

CMD ["uvicorn","main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["python3","-u", "main.py"]