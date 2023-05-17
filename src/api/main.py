#from elastic.connect_Elastic import connect_elastic_server
import json
from fastapi import FastAPI
from elastic.request_elasticsearch import router
from request_NYT.articles_functions import get_article
from elastic.connect_Elastic import connect_elastic_server, push_database


with open("ressources/mapping.json") as json_data_file:
    mapping = json.load(json_data_file)

es = connect_elastic_server()
app = FastAPI(title="NYT API")
app.include_router(router)

#def request_NYT(years,mounth,index_name):

    #data = get_article(years,mounth,index_name)
    #push_database(es,data,"article",mapping)
    #try :
        #create_database(es, "data_brutes/data_articles/nyt.csv","article", mapping)
    #except :
        #print("Il existe déjà une base de donnée")

    # stop after 1 or 2 "response ok"
    # si l'algo se stop, une boucle de create_tab_books s'est arreté, verifier alors si une table est apparu dans les bdd
    # si oui alors exceuter juste create_tab_article()

@app.get("/")
async def root():
    return {"message":"lol"}




