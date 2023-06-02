FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install fastapi uvicorn

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /code

#COPY . request_NYT/
#COPY . elastic/
#COPY . ressources/
#COPY . main.py

COPY . /code/app

WORKDIR /code/app
EXPOSE 8000

CMD ["python3", "main.py"]


