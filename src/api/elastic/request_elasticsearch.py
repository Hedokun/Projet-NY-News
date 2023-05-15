import json
from datetime import datetime

from .connect_Elastic import connect_elastic_server
from fastapi import APIRouter

with open("./ressources/request.json") as json_data_file:
    config = json.load(json_data_file)





router = APIRouter()
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

@router.get("/get_count_article/")
def get_count_article_range2(param):
    request = config["get_count_filter"]
    request['query']["bool"]["must"][0]['match']['Titres'] = param
    date = []
    count = []
    result_request = es.search(index='article', body=request, filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    d = {'Date': date, 'Count': count}
    return d

@router.get("/get_last_news/")
def get_last_news():
    request_last_news = config["get_last_news"]
    title = []
    url = []
    result_request = es.search(index='article', body=request_last_news, filter_path=["hits.hits"])
    for i in result_request["hits"]["hits"]:
        title.append(i["_source"]["Titres"])
        url.append(i["_source"]['web_url'])
    d = {'Title': title, 'Url': url}
    return d

@router.get("/get_time_bdd/")
def get_time_bdd():
    request_time_bdd = config['get_time_bdd']
    result_request = es.search(index='article', body=request_time_bdd, filter_path=["aggregations"])
    min_time = datetime.strptime(result_request['aggregations']["min_date"]["value_as_string"], "%Y-%m-%d")
    max_time = datetime.strptime(result_request['aggregations']["max_date"]["value_as_string"], "%Y-%m-%d")
    d = {'min_time': min_time, 'max_time': max_time}
    return d

@router.get("/get_top10/")
def get_top_ten_categorie():
    request_top_ten_categories = config["get_top_ten_categorie"]
    count = []
    keyword = []
    result_request = es.search(index='article', body=request_top_ten_categories,
                                          filter_path=["aggregations.group_by_categories.buckets"])
    for i in result_request["aggregations"]["group_by_categories"]["buckets"]:
        count.append(i["doc_count"])
        keyword.append(i["key"])
    d = {'Keyword': keyword, "Count": count}
    return d

@router.get("/get_cat_by_day/")
def get_cat_by_day(param):
    date = []
    count = []
    requests_get_cat_by_day = config["get_cat_by_day"]
    requests_get_cat_by_day['query']["bool"]["must"][0]['match']['categories'] = param
    result_request = es.search(index='article', body=requests_get_cat_by_day, filter_path=["aggregations"])
    for i in result_request["aggregations"]["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    d = {'Date': date, 'Count': count}
    return d


@router.post("/date_range_picker")
def get_date_range_picker():

    return
