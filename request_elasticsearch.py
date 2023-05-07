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

    return elasticsearch.search(index='article', body=request, filter_path=["aggregations.group_by_date.buckets"])


print(get_count_article_range(es, req))
