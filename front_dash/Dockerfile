FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip \
    pip install wheel
    
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD dashboard.py /my_dash/dashboard.py

WORKDIR /my_dash/
EXPOSE 8000

CMD python3 dashboard.py
