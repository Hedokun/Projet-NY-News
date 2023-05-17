import unittest
import os
import json

#import data_brutes.data_articles
import elastic.connect_Elastic
import elastic.request_elasticsearch
import main
import request_NYT.articles_functions

class testApp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(testApp, self).__init__(*args, **kwargs)
        self.es = elastic.connect_Elastic.connect_elastic_server()
        with open("./ressources/request.json") as json_data_file:
            self.config = json.load(json_data_file)

    def test_get_api_archive(self):
        """
        teste l'appel à l'APi NYT archive
        :return:
        """
        response = request_NYT.articles_functions.get_api_archive(2023,1)
        self.assertEqual(str(response), "<Response [200]>")


    def test_existing_bdd_bruts(self):
        """
        teste l'existence d'une base de données
        :return:
        """
        self.assertNotEqual(len(os.listdir("data_brutes/data_articles/")), 0)



    def test_connect_es(self):
        """
        teste la connection à elasticsearch
        :return:
        """
        self.assertEqual(self.es.ping(),True)


    def test_get_root_es(self):
        """
        teste la requete '*/*' de elasticsearch
        :return:
        """
        self.assertEqual(main.root(), "lol")

    def tes_get_count_article_es(self):
        """
        teste la requete get_count_article de elasticsearch
        obj: verifierr si ça renvoi 2 lists ?
        :return:
        """
        self.assertEqual(True, False)

    def test_get_last_news_es(self):
        """
        teste la requete get_last_news de elasticsearch
        :return:
        """
        request_last_news = self.config["get_last_news"]
        result_request = self.es.search(index='article', body=request_last_news, filter_path=["hits.hits"])
        self.assertEqual(str(result_request), "<Response [200]>")

    def test_get_time_bdd_es(self):
        """
        teste la requete get_time_bdd de elasticsearch
        :return:
        """
        request_time_bdd = self.config['get_time_bdd']
        result_request = self.es.search(index='article', body=request_time_bdd, filter_path=["aggregations"])
        self.assertEqual(str(result_request), "<Response [200]>")


    def test_get_top10_es(self):
        """
        teste la requete get_top10 de elasticsearch
        :return:
        """
        request_top_ten_categories = self.config["get_top_ten_categorie"]
        result_request = self.es.search(index='article', body=request_top_ten_categories,
                                   filter_path=["aggregations.group_by_categories.buckets"])
        self.assertEqual(str(result_request), "<Response [200]>")

    def test_date_range_picker_es(self):
        """
        teste la requete date_range_picker de elasticsearch
        :return:
        """
        self.assertEqual(True, False)

    def test_get_all_data_dash(self):
        """
        teste la fonction get_all_data de dash
        1) verifie que chaque reponse renvoi qqchose
        :return:
        """
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()

