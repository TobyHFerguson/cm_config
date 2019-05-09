FROM python:2-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY python/* /
CMD ["bin/sh"]
