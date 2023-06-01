from elasticsearch import Elasticsearch, helpers
import csv
import json

with open("./ressources/config_elastic_connet.json") as json_data_file:
    config = json.load(json_data_file)

with open("./ressources/mapping.json") as json_data_file:
    mapping = json.load(json_data_file)

ELASTIC_PASSWORD = config["ELASTIC_PASSWORD"]
ip = config["route_acces"]["ip"]
port = config["route_acces"]["port"]



def connect_elastic_server():
    """
    Fait la connexion avec le serveur de elasticsearch
    """
    es = Elasticsearch(hosts=f"https://{ip}:{port}",
                       http_auth=("elastic", ELASTIC_PASSWORD))
    return es



def connect_elastic_docker_server():
    es = Elasticsearch(hosts=f"https://elastic:datascientest@127.0.0.1:9200", ca_certs="./ressources/ca/ca.crt")
    return es


def push_database(elasticsearch, data, tablename):
    if elasticsearch.indices.exists(index=tablename):
        update_database(elasticsearch, data, tablename)
    else:
        create_database_bulker(elasticsearch, data, tablename)


def create_database_bulker(elasticsearch, data, tablename):
    """
    Créer la BDD elasticsearch avec un mapping précis lorsque la BDD n'est pas un csv
    :elasticsearch : connect_elastic_server()
    :data : 
    :tablename : 
    :setting :
    """
    elasticsearch.indices.create(index=tablename, body=mapping)
    helpers.bulk(elasticsearch, data, tablename)


def update_database(elasticsearch, data, tablename):
    """
    Met à jour la base de données sur elasticsearch
    :elasticsearch : connect_elastic_server()
    :data : 
    :tablename : 
    """
    helpers.bulk(elasticsearch, data, tablename)



def create_database_with_csv(elasticsearch, filepath, tablename, setting):
    """
    Créer la BDD elasticsearch avec un mapping précis lorsque la BDD est un csv
    :elasticsearch : connect_elastic_server()
    :filepath : str
    :tablename : 
    :setting :
    """
    elasticsearch.indices.create(index=tablename, body=setting)

    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(elasticsearch, reader, index=tablename)


def update_database_with_csv(elasticsearch, filepath, tablename, setting):
    """
    Met à jour la base de données sur elasticsearch lorsque la BDD est un csv
    :elasticsearch : connect_elastic_server()
    :filepath : str
    :tablename :
    :setting : 
    """
    elasticsearch.indices.update(index=tablename, body=setting)

    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(elasticsearch, reader, index=tablename)

