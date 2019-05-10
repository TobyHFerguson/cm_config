FROM python:2-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY python/* /
COPY bin/run.sh /
ENTRYPOINT ["/bin/sh", "run.sh"]
