import json
from datetime import datetime

from connect_Elastic import connect_elastic_server

with open("ressources/request.json") as json_data_file:
    config = json.load(json_data_file)


es = connect_elastic_server()

def get_count_article_range(elasticsearch, request):
    date = []
    count = []
    result_request = elasticsearch.search(index='article', body=request,
                                          filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    return date, count


def get_count_article_range2(elasticsearch, param):
    request = config["get_count_filter"]
    request['query']["bool"]["must"][0]['match']['Titres'] = param
    date = []
    count = []
    result_request = elasticsearch.search(index='article', body=request, filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    return date, count


def get_last_news(elasticsearch):
    request_last_news = config["get_last_news"]
    title = []
    url = []
    result_request = elasticsearch.search(index='article', body=request_last_news, filter_path=["hits.hits"])
    for i in result_request["hits"]["hits"]:
        title.append(i["_source"]["Titres"])
        url.append(i["_source"]['web_url'])
    return title, url


def get_time_bdd(elasticsearch):
    request_time_bdd = config['get_time_bdd']
    result_request = elasticsearch.search(index='article', body=request_time_bdd, filter_path=["aggregations"])
    min_time = datetime.strptime(result_request['aggregations']["min_date"]["value_as_string"], "%Y-%m-%d")
    max_time = datetime.strptime(result_request['aggregations']["max_date"]["value_as_string"], "%Y-%m-%d")
    return min_time, max_time


def get_top_ten_categorie(elasticsearch):
    request_top_ten_categories = config["get_top_ten_categorie"]
    count = []
    keyword = []
    result_request = elasticsearch.search(index='article', body=request_top_ten_categories,
                                          filter_path=["aggregations.group_by_categories.buckets"])
    for i in result_request["aggregations"]["group_by_categories"]["buckets"]:
        count.append(i["doc_count"])
        keyword.append(i["key"])
    return keyword, count
