FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install fastapi uvicorn

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY . request_NYT/
COPY . elastic/
COPY . ressources/
#ADD main.py
#ADD test_App.py
#ADD articles_functions.py /request_NYT/articles_functions.py
#ADD books_functions.py /request_NYT/books_functions.py
#ADD connect_Elastic.py elastic/connect_Elastic.py
#ADD request_elasticsearch.py elastic/request_elasticsearch.py
#ADD config_elastic_connet.json ressources/config_elastic_connet.json
#ADD mapping.json ressources/mapping.json
#ADD request.json ressources/request.json

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
#CMD python3 main.py
