FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install fastapi uvicorn

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /code

COPY . /code/app

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]


