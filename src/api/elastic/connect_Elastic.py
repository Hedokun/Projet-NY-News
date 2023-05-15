from elasticsearch import Elasticsearch, helpers
import csv
import json

with open("./ressources/config_elastic_connet.json") as json_data_file:
    config = json.load(json_data_file)

ELASTIC_PASSWORD = config["ELASTIC_PASSWORD"]
ip = config["route_acces"]["ip"]
port = config["route_acces"]["port"]


def connect_elastic_server():
    # Found in the 'Manage Deployment' page
    es = Elasticsearch(hosts=f"https://{ip}:{port}",
    http_auth=("elastic", ELASTIC_PASSWORD))
    return es


# Create the client instance




def create_database(elasticsearch, filepath, tablename, setting):
    elasticsearch.indices.create(index=tablename, body=setting)

    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(elasticsearch, reader, index=tablename)


def create_database_json(elasticsearch, data, tablename, setting):
    elasticsearch.indices.create(index=tablename, body=setting)
    data = csv.DictReader(data)
    helpers.bulk(elasticsearch, data,index=tablename)
    print("finis")
    #helpers.bulk(elasticsearch, data, index=tablename)

def update_database(elasticsearch, filepath, tablename, setting):
    elasticsearch.indices.update(index=tablename, body=setting)

    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(elasticsearch, reader, index=tablename)

