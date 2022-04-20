FROM python:3.8-slim-buster

COPY get_latest_artifact.py get_latest_artifact.py 
ENTRYPOINT [ "get_latest_artifact.py" ]