#!/usr/bin/env bash
# start-server.sh
#(cd app; gunicorn -w ${UVICORN_WORKERS:-3} --worker-class uvicorn.workers.UvicornWorker --timeout 300 -b 0.0.0.0:8080 views:app --keep-alive 300)

#(cd app; uvicorn views:app --proxy-headers --host 0.0.0.0 --port 8080 --timeout-keep-alive 3600 --timeout-graceful-shutdown 3600 --workers 8 --limit-max-requests 1 --loop uvloop)

(cd app; uvicorn views:app --proxy-headers --host 0.0.0.0 --port 8080 --timeout-keep-alive 3600 --timeout-graceful-shutdown 3600 --workers 8 --loop uvloop)