import csv
import json
import pandas as pd

with open("data_kibana/resultats.json") as json_data_file:
    res = json.load(json_data_file)


def count_article(response_get_article_range):
    data = pd.DataFrame(columns=['date', 'count'])
    try:
        for i in response_get_article_range['aggregations']["group_by_date"]["buckets"]:
            new_data = pd.DataFrame([(i['key_as_string'], i["doc_count"])], columns=['date', 'count'])
            data = pd.concat([data, new_data], ignore_index=True)
    except:
        print("erreur tab")
        pass

    return data
