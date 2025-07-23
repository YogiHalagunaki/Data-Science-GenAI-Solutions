# #!/usr/bin/env bash

# python app/run.py
#!/usr/bin/env bash

(cd app; gunicorn wsgi --user www-data --bind 127.0.0.1:8080 --workers 3 --worker-class=gevent --timeout=600) &
nginx -g "daemon off;"
