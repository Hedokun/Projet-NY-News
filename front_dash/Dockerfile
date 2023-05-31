FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD front_dash/dashboard.py /my_dash/dashboard.py
WORKDIR /my_dash/

EXPOSE 5000

CMD python3 dashboard.py
#CMD gunicorn -b 127.0.0.1:8000 dashboard:server