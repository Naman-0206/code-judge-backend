FROM my-ubuntu-image

WORKDIR /server

COPY . /server

RUN pip3 install -r requirements.txt

CMD ["python3","-u", "main.py"]