FROM python:3.10-slim-bullseye
EXPOSE 6868/tcp

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
RUN mkdir app
COPY ./run.py app
copy ./lib app/lib
copy ./pic app/pic

CMD cd app && python3 -m run