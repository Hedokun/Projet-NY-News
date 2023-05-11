import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash

app = JupyterDash(__name__)

# créer une mise en page
app.layout = html.Div([
    html.H1('Recherche d\'articles du New York Times'),
    dcc.Input(id='mot-recherche', type='text', placeholder='Entrez le mot à rechercher'),
    dcc.Graph(id='graphique')
])






df = pd.read_csv('data_brutes/data_articles/nyt.csv')


# definir une fonction de rappel pour mettre à jour le graphique en fonction du mot de recherche
@app.callback(
    dash.dependencies.Output('graphique', 'figure'),
    [dash.dependencies.Input('mot-recherche', 'value')])
def update_graph(mot_recherche):
    # filtrer les articles qui contiennent le mot recherché dans leur keyword
    df_filtre = df[df['keywords'].str.contains(mot_recherche, case=False)]

    # convertir la colonne pub_date en datetime et extraire la date
    df_filtre['date'] = pd.to_datetime(df_filtre['pub_date']).dt.date

    # regrouper les articles par date et compter le nombre d'articles pour chaque date
    df_group = df_filtre.groupby('date').size().reset_index(name='count')

    # graphique avec plotly
    fig = px.line(df_group, x='date', y='count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche))

    return fig
def create_dashboard():
    app.run_server(mode='inline')

# lancé Dash avec Jup

