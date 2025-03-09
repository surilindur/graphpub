FROM python:alpine

ADD graphpub /opt/graphpub
ADD requirements.txt /opt/graphpub/requirements.txt

WORKDIR /opt/graphpub

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]
