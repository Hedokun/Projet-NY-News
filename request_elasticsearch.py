from connect_Elastic import connect_elastic_server

req = {
    "query": {
        "range": {
            "pub_date": {
                "gt": "2020-01-01",
                "lt": "2020-01-21"
            }
        }
    },
    "aggs": {
        "group_by_date": {
            "date_histogram": {
                "field": "pub_date",
                "calendar_interval": "day",
                "format": "yyyy-MM-dd"
            }
        }
    }
}

es = connect_elastic_server()


def get_count_article_range(elasticsearch, request):
    date = []
    count = []
    result_request = elasticsearch.search(index='article', body=request, filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"] :
        print(i['key_as_string'])
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    return date,count



print(get_count_article_range(es, req))


def get_count_article_range2(elasticsearch,param):
    name = param
    date = []
    count = []
    req = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "Titres": name
                        }
                    }
                ],
                "filter": [
                    {
                        "range": {
                            "pub_date": {
                                "gte": "2020-01-01",
                                "lte": "2020-01-25"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "group_by_date": {
                "date_histogram": {
                    "field": "pub_date",
                    "calendar_interval": "day",
                    "format": "yyyy-MM-dd"
                }
            }
        }
    }
    result_request = elasticsearch.search(index='article', body=req, filter_path=["aggregations.group_by_date.buckets"])
    for i in result_request['aggregations']["group_by_date"]["buckets"] :
        print(i['key_as_string'])
        date.append(i['key_as_string'])
        count.append(i["doc_count"])
    return date,count

