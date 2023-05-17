import requests
import pandas as pd

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

def create_bulked_data(response,index_name):
    bulked_data = []
    for article in response:
        keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
        try:
            doc = {
                'Titres': article['headline']['main'],
                'doc_type': article['document_type'],
                'material_type': article['type_of_material'],
                'abstract': article['abstract'],
                'source': article['source'],
                'web_url': article['web_url'],
                'categories': article['section_name'],
                'lead_paragraph': article['lead_paragraph'],
                'pub_date': article["pub_date"],
                'keywords': keywords}
            data_dict = {
                "_index": index_name,
                "_source": doc}
            bulked_data.append(data_dict)
        except Exception as e:
            print(e)
    return bulked_data

def get_article(years,mounth,index_name):
    response = get_api_archive(years,mounth)
    extract = get_response(response)
    bulkded_data = create_bulked_data(extract,index_name)
    return bulkded_data