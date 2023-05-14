import json

import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash
import requests


url_api = "http://127.0.0.1:8000/"
app = JupyterDash(__name__)

# créer une mise en page
app.layout = html.Div([
    html.H1('Recherche d\'articles du New York Times'),
    dcc.Input(id='mot-recherche', type='text', placeholder='Entrez le mot à rechercher'),
    dcc.Graph(id='graphique')
])



def get_all_data():
    response = requests.get(url_api+f"get_time_bdd/")
    reponse_get_time_bdd = json.loads(response.content.decode())

    response = requests.get(url_api+f"get_last_news/")
    reponse_get_last_news = json.loads(response.content.decode())
    
    response = requests.get(url_api+f"get_top10/")
    reponse_get_top10 = json.loads(response.content.decode())

    return reponse_get_top10,reponse_get_last_news,reponse_get_time_bdd



def update_date(filter):
    response = requests.get(url_api+f"get_count_article/?param={filter}")
    reponse_parse = json.loads(response.content.decode())
    df = pd.DataFrame(reponse_parse)
    return df


# definir une fonction de rappel pour mettre à jour le graphique en fonction du mot de recherche
@app.callback(
    dash.dependencies.Output('graphique', 'figure'),
    [dash.dependencies.Input('mot-recherche', 'value')])
def update_graph(mot_recherche):
    if mot_recherche== None :
        mot_recherche = "France"
    data = update_date(mot_recherche)
    # graphique avec plotly
    fig = px.line(data, x='Date', y='Count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche))

    return fig


def create_dashboard():
    app.run_server(mode='inline')


# lancé Dash avec Jup
create_dashboard()

