FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
  python-pip \
  git

RUN pip install \
  requests \
  wheel

ENV SID="##"
ENV TOKEN="##"
