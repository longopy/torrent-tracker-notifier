FROM python:3.11-alpine
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
