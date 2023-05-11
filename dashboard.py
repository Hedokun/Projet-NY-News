import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash
from connect_Elastic import  connect_elastic_server
from request_elasticsearch import get_count_article_range2

app = JupyterDash(__name__)

# créer une mise en page
app.layout = html.Div([
    html.H1('Recherche d\'articles du New York Times'),
    dcc.Input(id='mot-recherche', type='text', placeholder='Entrez le mot à rechercher'),
    dcc.Graph(id='graphique')
])


es = connect_elastic_server()

def update_date(filter):
    date, count = get_count_article_range2(es, filter)
    d = {'Date': date, 'Count': count}
    df = pd.DataFrame(d)
    print(df)
    return df


# definir une fonction de rappel pour mettre à jour le graphique en fonction du mot de recherche
@app.callback(
    dash.dependencies.Output('graphique', 'figure'),
    [dash.dependencies.Input('mot-recherche', 'value')])
def update_graph(mot_recherche):
    data = update_date(mot_recherche)

    # graphique avec plotly
    fig = px.line(data, x='Date', y='Count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche))

    return fig


def create_dashboard():
    app.run_server(mode='inline')


# lancé Dash avec Jup

