import unittest
import os
import json
import aiounittest
from unittest.mock import patch

import elastic.connect_Elastic
import elastic.request_elasticsearch
import main
import request_NYT.articles_functions


class testApp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(testApp, self).__init__(*args, **kwargs)
        self.es = elastic.connect_Elastic.connect_elastic_server()
        with open("./ressources/requesttest.json") as json_data_file:
            self.config = json.load(json_data_file)

    def test_get_api_archive(self):
        """
        teste l'appel à l'APi NYT archive
        :return:
        """
        response = request_NYT.articles_functions.get_api_archive(2023, 1)
        self.assertEqual(str(response), "<Response [200]>")


    def test_connect_es(self):
        """
        teste la connection à elasticsearch
        :return:
        """
        self.assertEqual(self.es.ping(), True)

    @patch('requests.post')
    def test_post_data_to_database(self, mock_post):
        """
        teste la requete post_data_to_database de elasticsearch
        :return:
        """
        data = {'_index': 'article',
                '_source': {'Titres': "J'aime les chips",
                            'doc_type': 'article',
                            'material_type': 'News',
                            'abstract': "les pringels paprika sont les meilleurs",
                            'source': 'The New York Times',
                            'web_url': 'https://www.nytimes.com/2020/01/31/sports/olympics/toto.html',
                            'categories': 'Sports',
                            'lead_paragraph': 'lifetime ban.',
                            'pub_date': '2020-01-31T23:34:54+0000',
                            'keywords': ['chips', 'DataScientest']}}
        #test = elastic.connect_Elastic.push_database(self.es, data, "article")
        #mock_post.assert_called_with(self.es, data, "article")

    def test_get_count_article_es(self):
        """
        teste la requete get_total_count_article de elasticsearch
        :return:
        """
        res = elastic.request_elasticsearch.get_total_count_article("2020-01-26", "2020-01-26")
        self.assertEqual(res["Count"][0], 101)

    def test_get_count_filter_article_es(self):
        """
        teste la requete get_count_filter_article de elasticsearch
        :return:
        """
        res = elastic.request_elasticsearch.get_count_filter_article("Biden", "2020-01-26", "2020-01-26")
        self.assertEqual(res["Count"][0], 1)

    def test_get_last_news_es(self):
        """
        teste la requete get_last_news de elasticsearch
        longueur de _source doit être >0
        :return:
        """
        request_last_news = self.config["get_last_news"]
        result_request = self.es.search(index='article', body=request_last_news, filter_path=["hits.hits"])
        self.assertNotEqual(len(result_request['hits']['hits']), 0)

    def test_get_time_bdd_es(self):
        """
        teste la requete get_time_bdd de elasticsearch
        :return:
        """
        request_time_bdd = self.config['get_time_bdd']
        result_request = self.es.search(index='article', body=request_time_bdd, filter_path=["aggregations"])
        self.assertNotEqual(len(result_request["aggregations"]["max_date"]), 0)
        self.assertNotEqual(len(result_request["aggregations"]["min_date"]), 0)

    def test_get_top10_es(self):
        """
        teste la requete get_top10 de elasticsearch
        longueur de buckets doit être >0
        :return:
        """
        request_top_ten_categories = self.config["get_top_ten_categorie"]
        result_request = self.es.search(index='article', body=request_top_ten_categories,
                                        filter_path=["aggregations.group_by_categories.buckets"])
        self.assertNotEqual(len(result_request['aggregations']["group_by_categories"]["buckets"]), 0)

    def test_get_categories_count_by_day(self):
        """
        teste la fonction get_categories_count_by_day de elasticsearch
        :return:
        """
        res = elastic.request_elasticsearch.get_categories_count_by_day("U.S", "2020-01-26", "2020-01-26")
        self.assertEqual(res["Count"][0], 40)

    def test_get_all_data_dash(self):
        """
        teste la fonction get_all_data de dash
        1) verifie que chaque reponse renvoi qqchose
        :return:
        """
        #print(front_dash.dashboard.get_all_data()[1])
        #self.assertEqual(front_dash.dashboard.get_all_data()[1], True)


class testApp_async(aiounittest.AsyncTestCase):
    async def test_get_root_es(self):
        """
        teste la requete '*/*' de elasticsearch
        :return:
        """
        res = await main.root()
        self.assertEqual(res, {'message': "Bienvenue sur l'API NY-Time-News"})


if __name__ == '__main__':
    unittest.main()


