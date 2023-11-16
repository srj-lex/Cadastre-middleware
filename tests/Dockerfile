FROM python:3.9

WORKDIR /tests

RUN pip install requests --no-cache-dir

COPY . .

CMD python3 tests.py