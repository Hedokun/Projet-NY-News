import os
from articles_functions import create_tab_article_to_csv
import books_functions
from connect_Elastic import connect_elastic_server, create_database
import json

with open("resources/mapping.json") as json_data_file:
    mapping = json.load(json_data_file)


def create_bdd():
    # books_functions.create_tab_list_names()
    # books_functions.create_tab_books()
    create_tab_article_to_csv()
    es = connect_elastic_server()
    create_database(es, "data_brutes/data_articles/nyt.csv" "article", mapping)

    # stop after 1 or 2 "response ok"
    # si l'algo se stop, une boucle de create_tab_books s'est arreté, verifier alors si une table est apparu dans les bdd
    # si oui alors exceuter juste create_tab_article()


if __name__ == "__main__":
    # if len(os.listdir('data_brutes/data_books')) == 0:
    create_bdd()
