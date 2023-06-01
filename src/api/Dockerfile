FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install fastapi uvicorn

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
#COPY . request_NYT/
#COPY . elastic/
#COPY . ressources/

#CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]

CMD uvicorn main:app --reload
