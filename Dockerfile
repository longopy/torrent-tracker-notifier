FROM python:3.11-alpine

RUN apk add --no-cache bash curl dcron

COPY app //opt/app/
WORKDIR /opt/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]