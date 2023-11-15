FROM python:3.9

WORKDIR /cadstre_middleware

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD python3 cadastre_server.py