# Dockerfile
FROM  /home/yogi/python:3.10-slim

# copy source and install dependencies
RUN mkdir -p /opt/Documents_Digitization_Process/app
COPY requirements.txt start-server.sh /opt/Documents_Digitization_Process/
COPY app /opt/Documents_Digitization_Process/app

WORKDIR /opt/Documents_Digitization_Process

RUN apt update -y && apt-get upgrade -y \
    # && apt-get install nginx -y --no-install-recommends \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt && pip cache purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
	&& chmod 777 -R /opt/Documents_Digitization_Process

# RUN rm /etc/apt/sources.list
# RUN echo "deb http://archive.debian.org/debian-security jessie/updates main" > /etc/apt/sources.list.d/jessie.list

# setup nginx 
# COPY nginx.default /etc/nginx/sites-available/default

# start server
EXPOSE 80
EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["bash", "/opt/Documents_Digitization_Process/start-server.sh"]
