FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD python3 dashboard.py
CMD gunicorn -b 127.0.0.1:8000 dashboard:server
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]