FROM ubuntu:latest

MAINTAINER Daniel Kovalenko "animtel@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

EXPOSE 5000

CMD [ "startup.py" ]