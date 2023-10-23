FROM python:3.10

WORKDIR /calistopia

COPY . .

RUN pip install -r requirements.txt

