import requests
from datetime import datetime
import pandas as pd
from numpy import NAN
import os
from datetime import date


def filter_by_day(list, day):
    result = []
    for article in list:
        d = datetime.strptime(article["pub_date"], "%Y-%m-%dT%H:%M:%S%z")
        if d.day == day:
            result.append(article)
    return result


def get_api_archive(year, month):
    """
    récupère tous les articles d'un mois précis
    :param year: int
    :param month: int
    :return: requete
    """
    api = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=eOrVnjKORoQABwkzbpKiRef1i8Lh4X9G"
    response = requests.get(api)
    return response



def get_response(response):
    """
    transforme get_api_archive en dictionnaire
    :param response:
    :return: dict
    """
    data= response.json()
    articles=data["response"]["docs"]
    return articles


def parse_response(response):
    'Créer un dataFrame des données utiles'
    data1 = {'Titres': [],
             'doc_type': [],
             'material_type': [],
             'abstract': [],
             'source': [],
             'web_url': [],
             'categories': [],
             'lead_paragraph': [],
             'pub_date': [],
             # 'sous_categories':[]
             'keywords': []
             }

    for article in response:
        data1['Titres'].append(article['headline']['main'])
        data1['abstract'].append(article['abstract'])
        data1['web_url'].append(article['web_url'])
        data1['lead_paragraph'].append(article['lead_paragraph'])
        data1['source'].append(article['source'])
        data1['pub_date'].append(article["pub_date"])
        data1['doc_type'].append(article['document_type'])
        data1['categories'].append(article['section_name'])
        data1['material_type'].append(article['type_of_material'])

        # data1['sous_categories'].append(article['subsection_name '])
        # data1["auteur"].append(article["byline"]["person"][0]["firstname"]+" "+article["byline"]["person"][0]["lastname"])
        keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
        data1['keywords'].append(keywords)

        df = pd.DataFrame(data1)

    return df

def order_by_key(df_article):
    """
    transforme data brut de parse_response en mots clé par ligne
    :param df_article: dataframe
    :return: dataframe
    """
    df_article['keywords'] = df_article['keywords'].apply(lambda x: x[1:-1].split(","))
    new_df = df_article.assign(key1=df_article['keywords'].apply(lambda x: x[0] if len(x) > 0 else NAN)) \
        .assign(key2=df_article['keywords'].apply(lambda x: x[1] if len(x) > 1 else NAN)) \
        .assign(key3=df_article['keywords'].apply(lambda x: x[2] if len(x) > 2 else NAN)) \
        .assign(key4=df_article['keywords'].apply(lambda x: x[3] if len(x) > 3 else NAN)) \
        .assign(key5=df_article['keywords'].apply(lambda x: x[4] if len(x) > 4 else NAN)) \
        .assign(key6=df_article['keywords'].apply(lambda x: x[5] if len(x) > 5 else NAN)) \
        .assign(key7=df_article['keywords'].apply(lambda x: x[6] if len(x) > 6 else NAN)) \
        .assign(key8=df_article['keywords'].apply(lambda x: x[7] if len(x) > 7 else NAN)) \
        .assign(key9=df_article['keywords'].apply(lambda x: x[8] if len(x) > 8 else NAN)) \
        .assign(key10=df_article['keywords'].apply(lambda x: x[9] if len(x) > 9 else NAN))\
        .assign(id= df_article.index)

    new_df.pop('keywords')
    return new_df


#def create_df_keys(df_order_by_key):
#    """
#    transforme df de order_by_key en table des tendances par mots clés
#    :param df_order_by_key: dataframe
#    :return: dataframe
#    """
#    df_keys = pd.wide_to_long(df_order_by_key, "key", i="id", j="keys") \
#        .dropna(subset=["key"]) \
#        .groupby(['key', 'pub_date'])['Titres'].count().sort_values(ascending=False).reset_index(name='count')# \
#        #.pivot(index="key", columns="pub_date", values="count")
#
#    return df_keys
#
#def create_df_categories(df_order_by_key):
#    """
#    transforme df de order_by_key en table des tendances par categories
#    :param df_order_by_key: dataframe
#    :return: dataframe
#    """
#    df_categories = df_order_by_key.groupby(['categories', 'pub_date'])['id'].count().sort_values(
#        ascending=False).reset_index(name='count')# \
#        #.pivot(index="categories", columns="pub_date", values="count")
#
#    return df_categories

#def count_keywords(df_order_by_key):
#    df_keys = pd.wide_to_long(df_order_by_key, "key", i="id", j="keys") \
#        .dropna(subset=["key"]) \
#        .groupby('key')['key'].count().sort_values(ascending=False).reset_index(name='count')
#
#    return df_keys

def create_tab_article(start_date,end_date):
    """
    Créer table brute article à partir des archives et renvoi en csv
    :return: /
    """
    from datetime import date
    #start_date = date(2018, 1, 1)
    #end_date = date(2023, 4, 1)
    daterange = pd.date_range(start_date, end_date, freq='M').sort_values(ascending=False)
    for date in daterange:
        if os.path.exists("data_brutes/data_articles/" + str(date)[0:7]+ "_nyt.csv"):
            pass
        else:
            try:
                response = get_response(get_api_archive(date.year,date.month))
                print("response ok")
                data = parse_response(response)
                data.to_csv("data_brutes/data_articles/" + str(date)[0:7]+"_nyt.csv", index=False,
                            header=True, sep=',')
            except:
                print("stop date: " + str(date))
                exit()


def merge_data(file1, file2=None):

    if os.path.exists("data_brutes/data_articles/articles_nyt.csv") and file2==None:
        file2 = 'data_brutes/data_articles/articles_nyt.csv'
        files = [file2, file1]
    else:
        files = [file1, file2]
    df = pd.DataFrame()
    if len(files) > 1:
        for file in files:
            data = pd.read_csv(file)
            df = pd.concat([df, data], axis=0)
        df.to_csv('data_brutes/data_articles/articles_nyt.csv', index=False)
        os.remove(file1)

def update_data(dash_start, dash_stop):

    formatting = "%Y-%m-%d"
    dash_start=datetime.strptime(dash_start, formatting).date()
    dash_stop=datetime.strptime(dash_stop, formatting).date()
    file = pd.read_csv('data_brutes/data_articles/articles_nyt.csv')
    min_date=min(file.pub_date)[0:10]
    max_date=max(file.pub_date)[0:10]
    min_date=datetime.strptime(min_date, formatting).date()
    max_date=datetime.strptime(max_date, formatting).date()

    if max_date<dash_stop:
        create_tab_article(max_date,dash_stop)
    if min_date> dash_start:
        create_tab_article(dash_start,min_date)

    directory = "data_brutes/data_articles/"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and f != 'data_brutes/data_articles/articles_nyt.csv':
            merge_data(f)
            print("data merge")



