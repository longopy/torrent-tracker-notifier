#!/bin/sh

echo "Configuring cron jobs..."

echo "$CRON_EXPRESSION cd /opt/app && python3 main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution

chmod 0644 /etc/cron.d/cron_execution

cat /etc/cron.d/cron_execution

echo "Running job immediately..."
cd /opt/app/ && python3 main.py >> /var/log/cron.log 2>&1

echo "Starting cron..."
crond -l 2 && tail -f /var/log/cron.log
