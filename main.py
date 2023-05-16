from create_bdd.articles_functions import create_tab_article
from connect_Elastic import connect_elastic_server, create_database
import json
from dashboard import create_dashboard,update_graph

with open("ressources/mapping.json") as json_data_file:
    mapping = json.load(json_data_file)

try :
    es = connect_elastic_server()
except :
    es = 0
def create_bdd():
    # books_functions.create_tab_list_names()
    # books_functions.create_tab_books()
    create_tab_article()
    try :
        create_database(es, "data_brutes/data_articles/nyt.csv","article", mapping)
    except :
        print("Il existe déjà une base de donnée")

    # stop after 1 or 2 "response ok"
    # si l'algo se stop, une boucle de create_tab_books s'est arreté, verifier alors si une table est apparu dans les bdd
    # si oui alors exceuter juste create_tab_article()

def connect_dash():

    create_dashboard()
    update_graph()

if __name__ == "__main__":
    # if len(os.listdir('data_brutes/data_books')) == 0:
    ##create_bdd()
    connect_dash()
