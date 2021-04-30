FROM python:slim-buster

WORKDIR /var/opt

COPY dashboard-requirements.txt /var/opt/requirements.txt

RUN pip install -r /var/opt/requirements.txt

COPY pvsimulator /var/opt/pvsimulator
COPY README.md /var/opt/README.md