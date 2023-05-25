FROM python:latest

RUN pip install --upgrade pip && \
    pip install aldryn_apphooks_config \
    pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python3 dashboard.py
