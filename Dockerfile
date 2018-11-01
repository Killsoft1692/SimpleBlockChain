FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-dev build-essential python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]
EXPOSE 8080
