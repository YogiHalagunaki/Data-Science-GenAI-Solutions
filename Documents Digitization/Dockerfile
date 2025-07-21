# Dockerfile
# Stage 1: Build
FROM python:3.10.16-slim-bookworm AS build

RUN useradd -ms /bin/bash 1000

# copy source and install dependencies
RUN mkdir -p /opt/Documents_Digitization_Process/app

COPY requirements.txt start-server.sh /opt/Documents_Digitization_Process/
COPY app /opt/Documents_Digitization_Process/app

WORKDIR /opt/Documents_Digitization_Process

RUN apt-get update -y && apt-get upgrade -y \
    && pip install --upgrade pip setuptools \
    && apt-get -y install tesseract-ocr \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
	&& pip cache purge

RUN python3 -m compileall -b . /opt/Documents_Digitization_Process/app \
    && find . -name "*.py" -type f -delete /opt/Documents_Digitization_Process/app/

# Stage 2: Runtime
FROM python:3.10.16-slim-bookworm

RUN apt-get update -y && apt-get upgrade -y

COPY --from=build /opt/Documents_Digitization_Process /opt/Documents_Digitization_Process

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

RUN chmod 777 -R /opt/Documents_Digitization_Process \
    && pip install --upgrade pip setuptools

WORKDIR /opt/Documents_Digitization_Process

# start server
EXPOSE 8080
STOPSIGNAL SIGTERM
USER 1000

ENTRYPOINT ["/bin/bash"]
CMD ["/opt/Documents_Digitization_Process/start-server.sh"]