from elasticsearch import Elasticsearch, helpers
import csv

Settings = {
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 2
  },
  "mappings": {
    "properties": {
      "Titres": {
        "type": "text"
      },
      "doc_type": {
        "type": "text"
      },
      "material_type": {
        "type": "text"
      },
      "abstract": {
        "type": "text"
      },
      "source": {
        "type": "text"
      },
      "web_url": {
        "type": "text"
      },
      "categories": {
        "type": "text"
      },
      "lead_paragraph": {
        "type": "text"
      },
      "pub_date": {
        "type": "date"
      },
      "keywords": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}

def connect_elastic():
    es = Elasticsearch(hosts="https://elastic:datascientest@localhost:9200", ca_certs="ca/ca.crt")

    print(es.ping())

    es.indices.create(index="article", body=Settings)

    with open("data_brutes/data_articles/nyt.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index="article")



connect_elastic()
