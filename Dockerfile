FROM python:3.10-slim-bullseye
EXPOSE 6868/tcp

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY run.py ./app
copy lib ./app
copy pic ./app