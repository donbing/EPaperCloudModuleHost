FROM python:3.10.8-alpine3.16
EXPOSE 6868/tcp

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./run.py app
COPY ./pqf app
COPY ./lib app/lib
COPY ./pic app/pic

WORKDIR /app
CMD ["python3", "-m", "run"]
