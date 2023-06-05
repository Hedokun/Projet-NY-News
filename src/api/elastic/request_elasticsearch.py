import json
from datetime import datetime
import sys

sys.path.append("..")
from request_NYT.articles_functions import get_article
from .connect_Elastic import connect_elastic_docker_server, push_database,connect_elastic_server, create_database_bulker
from fastapi import APIRouter
import pandas as pd

with open("./ressources/request.json") as json_data_file:
    config = json.load(json_data_file)

router = APIRouter()

es = connect_elastic_server()


@router.post('/post_data_to_database/', tags=['data'])
def post_data_to_database(years, month):
    data = get_article(years, month, "article")
    push_database(es, data, "article")


def get_count_article_range(elasticsearch, request):

    date = []
    count = []
    result_request = elasticsearch.search(index='article', body=request,
                                          filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    return date, count


@router.get("/get_total_count_article/", tags=['data'])
def get_total_count_article(min_date, max_date):
    """
    Retourne pour chaque jour d'un interval, le nombre d'articles parus sur le site du Ny-Times
    """
    check_time(min_date, max_date)
    date = []
    count = []
    request = config["get_total_article_count"]
    request['query']["bool"]["filter"][0]['range']['pub_date']["gte"] = min_date
    request['query']["bool"]["filter"][0]['range']['pub_date']["lte"] = max_date
    result_request = es.search(index='article', body=request, filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    d = {'Date': date, 'Count': count}
    return d

@router.get("/get_count_filter_article/", tags=['data'])
def get_count_filter_article(param, min_date, max_date):
    """
    Retourne pour chaque jour d'un interval, le nombre d'articles parus sur le site du Ny-Times contenant dans son titre le @param
    """
    check_time(min_date, max_date)
    date = []
    count = []
    request = config["get_count_filter"]
    request['query']["bool"]["must"][0]['match']['Titres'] = param
    request['query']["bool"]["filter"][0]['range']['pub_date']["gte"] = min_date
    request['query']["bool"]["filter"][0]['range']['pub_date']["lte"] = max_date
    result_request = es.search(index='article', body=request, filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    d = {'Date': date, 'Count': count}
    return d


@router.get("/get_last_news/", tags=['data'])
def get_last_news():
    """
    Renvois une liste contenant le titre et l'url des derniers articles insérés dans la base de donnée
    """
    request_last_news = config["get_last_news"]
    title = []
    url = []
    result_request = es.search(index='article', body=request_last_news, filter_path=["hits.hits"])
    for i in result_request["hits"]["hits"]:
        title.append(i["_source"]["Titres"])
        url.append(i["_source"]['web_url'])
    d = {'Title': title, 'Url': url}
    return d


@router.get("/get_time_bdd/", tags=['data'])
def get_time_bdd():
    """
    Récupère la date du plus vieil article et du plus récent article stockés en base
    """
    request_time_bdd = config['get_time_bdd']
    result_request = es.search(index='article', body=request_time_bdd, filter_path=["aggregations"])
    min_time = datetime.strptime(result_request['aggregations']["min_date"]["value_as_string"], "%Y-%m-%d")
    max_time = datetime.strptime(result_request['aggregations']["max_date"]["value_as_string"], "%Y-%m-%d")
    d = {'min_time': min_time, 'max_time': max_time}
    return d


@router.get("/get_top_ten_categorie/", tags=['data'])
def get_top_ten_categorie():
    """
    Renvoi une liste des 10 catégories d'article les plus présentes dans la base de données
    """
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


@router.get("/get_categories_count_by_day/", tags=['data'])
def get_categories_count_by_day(param, min_date, max_date):
    """
    Retourne pour une catégorie d'article et pour chaque jour d'un interval, le nombre d'articles parus sur le site du Ny-Times
    """
    check_time(min_date, max_date)
    date = []
    count = []
    requests_get_cat_by_day = config["get_cat_by_day"]
    requests_get_cat_by_day['query']["bool"]["must"][0]['match']['categories'] = param
    requests_get_cat_by_day['query']["bool"]["filter"][0]['range']['pub_date']["gte"] = min_date
    requests_get_cat_by_day['query']["bool"]["filter"][0]['range']['pub_date']["lte"] = max_date
    result_request = es.search(index='article', body=requests_get_cat_by_day, filter_path=["aggregations"])
    for i in result_request["aggregations"]["group_by_date"]["buckets"]:
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    d = {'Date': date, 'Count': count}
    return d


def check_time(dash_min, dash_max):
    """
    Récupère la date demandée par l'utilisateur et vérifie si les données sont présentes en base. Si non, requte sur l'API NYT et insère les données demandées dans la base
    """
    time = get_time_bdd()
    bdd_min = time["min_time"]
    bdd_max = time["max_time"]
    dash_min = datetime.strptime(dash_min, "%Y-%m-%d")
    dash_max = datetime.strptime(dash_max, "%Y-%m-%d")
    if dash_min < bdd_min:
        daterange = pd.date_range(dash_min, bdd_min, freq='M').sort_values(ascending=False)
        for i in daterange[:-1]:
            data = get_article(i.year, i.month, "article")
            push_database(es, data, "article")
    elif dash_max > bdd_max :
        daterange = pd.date_range(bdd_max, dash_max, freq='M').sort_values(ascending=False)
        for i in daterange[1:]:
            data = get_article(i.year, i.month, "article")
            push_database(es, data, "article")
    else:
        return
