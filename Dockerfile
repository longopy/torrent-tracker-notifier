FROM python:3.11-alpine

COPY app //opt/app/
WORKDIR /opt/app/

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]