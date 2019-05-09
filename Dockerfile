FROM python:rc-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["/bin/sh"]
