from  ElasticSearch.connect_Elastic import connect_elastic_server

class Elasticsearch:

    def __init__(self, date_start, date_stop,request):
        self.date_start = date_start
        self.date_stop = date_stop
        self.request = request



    def req_keyword_group_by_date(self):

        req = {
            "query": {
                "range": {
                    "pub_date": {
                        "gt": self.date_start,
                        "lt": self.date_stop
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

        return req

    def get_article_range(self,elasticsearch):
        try:
            response =elasticsearch.search(index='article', body=self.request,filter_path=["aggregations.group_by_date.buckets"])
        except:
            response = "erreur requete"
        return response


    def count_article(self,response_get_article_range):
        date = []
        count = []
        try:
            for i in response_get_article_range['aggregations']["group_by_date"]["buckets"]:
                print(i['key_as_string'])
                date.append(i['key_as_string'])
                count.append(i["doc_count"])
        except:
            print("erreur tab")
            pass
        return date, count


es = connect_elastic_server()
obj = Elasticsearch()
value = Elasticsearch.get_article_range(es, obj.req_keyword_group_by_date())
Elasticsearch.count_article(value)
