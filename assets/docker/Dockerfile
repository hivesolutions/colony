FROM ubuntu:latest
MAINTAINER Hive Solutions

RUN apt-get update
RUN apt-get install -y -q python python-setuptools wget
RUN easy_install pip
RUN pip install colony
RUN wget https://github.com/hivesolutions/config/raw/master/colony/base.txt
RUN cpm require base.txt
RUN rm base.txt

ENTRYPOINT usr/local/bin/colony
