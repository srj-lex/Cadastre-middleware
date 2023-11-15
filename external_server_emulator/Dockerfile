FROM python:3.9

WORKDIR /external_server_emulator

RUN pip install Flask --no-cache-dir

COPY . .

CMD python3 ext_server.py