# Stage 1: Build
FROM python:3.10.18-slim-bookworm AS build

RUN useradd -ms /bin/bash 1000 insurance-finance-doc-processing

# copy source and install dependencies
RUN mkdir -p /opt/insurance_finance_doc_processing/app

COPY requirements.txt start-server.sh /opt/insurance_finance_doc_processing/
COPY app /opt/insurance_finance_doc_processing/app

WORKDIR /opt/insurance_finance_doc_processing

RUN apt-get update -y && apt-get upgrade -y \
    && pip install --upgrade pip setuptools \
    && apt-get -y install tesseract-ocr \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
	&& pip cache purge

RUN python3 -m compileall -b . /opt/insurance_finance_doc_processing/app \
    && find . -name "*.py" -type f -delete `/opt/insurance_finance_doc_processing/app/`

# Stage 2: Runtime
FROM python:3.10.18-slim-bookworm

RUN apt-get update -y && apt-get upgrade -y

COPY --from=build /opt/insurance_finance_doc_processing /opt/insurance_finance_doc_processing

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

RUN chmod 777 -R /opt/insurance_finance_doc_processing \
    && pip install --upgrade pip setuptools

WORKDIR /opt/insurance_finance_doc_processing

# start server
EXPOSE 8080
STOPSIGNAL SIGTERM
USER 1000

ENTRYPOINT ["/bin/bash"]
CMD ["/opt/insurance_finance_doc_processing/start-server.sh"]
