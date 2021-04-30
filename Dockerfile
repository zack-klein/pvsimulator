FROM python:slim-buster

WORKDIR /var/opt

COPY requirements.txt /var/opt/requirements.txt

RUN pip install -r /var/opt/requirements.txt

COPY pvsimulator /var/opt/pvsimulator

# Needs unbuffered output!
# https://stackoverflow.com/a/29745541/14868936
# Final command will either be:
# python -u pvsimulator.py
# or
# python -u meter.py