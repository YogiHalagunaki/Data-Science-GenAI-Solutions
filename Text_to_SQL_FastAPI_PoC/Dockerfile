# Stage 1: Build
FROM python:3.10.18-slim-bookworm AS build

RUN useradd -ms /bin/bash 1000

# copy source and install dependencies
RUN mkdir -p /opt/Text_to_SQL_FastAPI_PoC/app

COPY requirements.txt start-server.sh /opt/Text_to_SQL_FastAPI_PoC/
COPY app /opt/Text_to_SQL_FastAPI_PoC/app

WORKDIR /opt/Text_to_SQL_FastAPI_PoC

RUN apt-get update -y && apt-get upgrade -y \
    && pip install --upgrade pip setuptools \
    && apt-get -y install tesseract-ocr \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
	&& pip cache purge

RUN python3 -m compileall -b . /opt/Text_to_SQL_FastAPI_PoC/app \
    && find . -name "*.py" -type f -delete `/opt/Text_to_SQL_FastAPI_PoC/app/`

# Stage 2: Runtime
FROM python:3.10.18-slim-bookworm

RUN apt-get update -y && apt-get upgrade -y

COPY --from=build /opt/Text_to_SQL_FastAPI_PoC /opt/Text_to_SQL_FastAPI_PoC

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

RUN chmod 777 -R /opt/Text_to_SQL_FastAPI_PoC \
    && pip install --upgrade pip setuptools

WORKDIR /opt/Text_to_SQL_FastAPI_PoC

# start server
EXPOSE 8080
STOPSIGNAL SIGTERM
USER 1000

ENTRYPOINT ["/bin/bash"]
CMD ["/opt/Text_to_SQL_FastAPI_PoC/start-server.sh"]
