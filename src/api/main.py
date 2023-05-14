#from elastic.connect_Elastic import connect_elastic_server
import json
from fastapi import FastAPI
from elastic.request_elasticsearch import router
from elastic.connect_Elastic import create_database
from request_NYT.articles_functions import create_tab_article

with open("ressources/mapping.json") as json_data_file:
    mapping = json.load(json_data_file)


app = FastAPI(title="NYT API")
app.include_router(router)
#def request_NYT():
    #es = connect_elastic_server()
    #create_tab_article()
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
