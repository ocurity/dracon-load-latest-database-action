FROM python:slim-buster

WORKDIR '/home/workdir'
COPY get_latest_artifact.py get_latest_artifact.py 
RUN pip3 install requests python-dateutil
ENTRYPOINT [ "python", "/home/workdir/get_latest_artifact.py" ]