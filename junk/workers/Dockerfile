FROM python:3.10-slim


# RUN sudo apt update
# RUN sudo apt install python3

WORKDIR /worker

COPY . .
RUN mkdir -p temp
RUN chmod 700  /
RUN chmod 755 -R temp/
RUN adduser --disabled-password --gecos "" judge

RUN python3 --version
# RUN pip3 install -r requirements.txt
CMD ["python3", "utils.py"]
