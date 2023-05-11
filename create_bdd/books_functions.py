import requests
from datetime import date, timedelta
import pandas as pd
import pickle
import os
from pynytimes import NYTAPI
import itertools


def get_api_list_name():
    """
    récupère tous les requetes des categories des livres
    :return: requete
    """
    response = requests.get(
        "https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=2U5DqnjNtPCugQHMyqV7RIGNG4f03mAK",
        timeout=10)
    return response

def get_api_books(date,name):
    """
    récupère tous le top des livres selon la classe et la date
    :param date: int
    :param name: string
    :return: requete
    """
    response = requests.get("https://api.nytimes.com/svc/books/v3/lists/" + str(date)[0:10] + "/" + name + ".json?api-key=2U5DqnjNtPCugQHMyqV7RIGNG4f03mAK",
                                      timeout=10)

    return response


def get_api_books_by_author(name):
    """
    récupère tous les livres d'un auteur
    :param prenom: string
    :param nom: string
    :return: list
    """
    nyt = NYTAPI("2U5DqnjNtPCugQHMyqV7RIGNG4f03mAK", parse_dates=True)
    books_nyt = nyt.book_reviews(author=name)

    return books_nyt


def get_list_name(response):
    list_name = []
    for i in response.json()["results"]:
        print(i["list_name_encoded"])
        list_name.append(i["list_name_encoded"])
    return list_name


def get_response(response):
    """
    transforme get_api_archive en dictionnaire
    :param response:
    :return: dict
    """
    data= response.json()
    books=data["results"]["books"]
    return books

def reponse_to_dataframe(response,date,name):
    """
    transforme la réponse de l'API en dataframe de la table brute
    :param response:
    :param date: date
    :param name: string
    :return: dataframe
    """
    data1 = {'date_response': [],
             'list_name': [],
             'rank': [],
             'rank_last_week': [],
             'publisher': [],
             'description': [],
             'title': [],
             'author': [],
             'buy_links': []}

    for book in response:
        data1['date_response'].append(str(date)[0:10])
        data1['list_name'].append(name)
        data1['rank'].append(book['rank'])
        data1['rank_last_week'].append(book['rank_last_week'])
        data1['publisher'].append(book['publisher'])
        data1['description'].append(book['description'])
        data1['title'].append(book['title'])
        data1['author'].append(book["author"])
        data1['buy_links'].append(book['buy_links'])
    return pd.DataFrame(data1)


def create_tab_list_names():
    """
    Stocke la liste des categories en base
    :return: /
    """
    try:
        list_names = get_list_name(get_api_list_name())
        fichier = open('../data_brutes/data_books/list_names.txt', 'wb')
        pickle.dump(list_names, fichier)
    except:
        print( "l'API a un problème")

def create_tab_books():
    """
    créer la table brute books et transforme en csv
    :return: /
    """
    from datetime import date
    start_date = date(2013, 1, 1)
    end_date = date(2023, 4, 1)
    daterange = pd.date_range(start_date, end_date, freq='W-SUN').sort_values(
        ascending=False)

    fichier_list_names = open('../data_brutes/data_books/list_names.txt', 'rb')
    list_names = pickle.load(fichier_list_names)
    for category in list_names:
        for date in daterange:
            if os.path.exists("data_brutes/data_books/"+ str(date)[0:10]+"_"+category+"_nyt.csv"):
                pass
            else:
                try:
                    response = get_response(get_api_books(str(date)[0:10], category))
                    data = reponse_to_dataframe(response, str(date)[0:10], category)
                    data.to_csv("data_brutes/data_books/"+ str(date)[0:10]+"_"+category+"_nyt.csv", index=False, header=True, sep=";")
                except:
                    print("stop date: "+str(date)+" categorie: "+category)
                    exit()


def get_author():


    list_author=[]

    from datetime import date
    start_date = date(2013, 1, 1)
    end_date = date(2023, 4, 1)
    daterange = pd.date_range(start_date, end_date, freq='W-SUN').sort_values(
        ascending=False)

    fichier_list_names = open('../data_brutes/data_books/list_names.txt', 'rb')
    list_names = pickle.load(fichier_list_names)
    for category in list_names:
        for date in daterange:
            if os.path.exists("data_brutes/data_books/"+ str(date)[0:10]+"_"+category+"_nyt.csv"):
                data=pd.read_csv("data_brutes/data_books/"+ str(date)[0:10]+"_"+category+"_nyt.csv", sep=";")
                auteurs=data['author'].tolist()
                for i in auteurs:
                    a = i.split(" and ")
                    list_author.append(a)

    list_author = list(itertools.chain(*list_author))
    list_author = list(set(list_author))
    fichier = open('../data_brutes/data_books/list_author.txt', 'wb')
    pickle.dump(list_author, fichier)





