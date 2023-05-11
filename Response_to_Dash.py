import csv
import json
import pandas as pd
from ElasticSearch.Elasticsearch_requests import Elasticsearch

es = connect_elastic_server()
obj = Elasticsearch()
value = Elasticsearch.get_article_range(es, obj.req_keyword_group_by_date())
Elasticsearch.count_article(value)


with open("data_kibana/resultats.json") as json_data_file:
    res = json.load(json_data_file)


class Response_to_Dash:
    def __init__(self, response):
        self.response = response

    def count_article(self):
        data = pd.DataFrame(columns=['date', 'count'])
        try:
            for i in self.response['aggregations']["group_by_date"]["buckets"]:
                new_data = pd.DataFrame([(i['key_as_string'], i["doc_count"])], columns=['date', 'count'])
                data = pd.concat([data, new_data], ignore_index=True)
        except:
            print("erreur tab")
            pass

        return data
