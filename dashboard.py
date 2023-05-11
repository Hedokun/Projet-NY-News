import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash
from connect_Elastic import  connect_elastic_server
from request_elasticsearch import get_count_article_range2
import dash_bootstrap_components as dbc
from datetime import date


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
colors = {
    'background': '#0D75FA',
    'text': '#FFFFFF'
}
style ={
    'TextAlign':"center",
    "colors" :"#FFFFF"
}
# créer une mise en page
app.layout = html.Div(children=[    
dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(href="#")),
    ],
    brand="New-York Time Dashboard",
    brand_href="#",
    color="#0D75FA",
    dark=True,
    links_left = True,
    class_name='mb-3'
),
    dbc.Row([
            dbc.Card(             
                dbc.CardBody(children = [
                    dbc.Col(dbc.Input(id='mot-recherche',placeholder="Entrez le mot à rechercher", type="text"),width=2,className="mb-1 rounded"),
                    dbc.Col(dcc.DatePickerRange(id='my-date-picker-range', min_date_allowed=date(1995, 8, 5), max_date_allowed=date(2023, 5, 11),initial_visible_month=date(2017, 8, 5), end_date=date(2017, 8, 25),className= "rounded"))
                
        ]),className="rounded shadow-sm p-4"),  
    ],className="p-3"),

    dbc.Row([
        dbc.Col( 
            dbc.Card(
            dbc.CardBody(children = [dcc.Graph(id='graphique-categories')]),className="shadow bg-white rounded",), width= "auto" ,className=' p-3 '
                )
       ,dbc.Col(
            dbc.Card(
                dbc.CardBody(children = [dcc.Graph(id='graphique-abstract')]),className="shadow bg-white rounded",), width= "auto",className='p-3'
                    )  
        ],
        ),
        dbc.Row([
            dbc.Card(dbc.CardBody(children =[dcc.Graph(id='graphique')]),className="shadow bg-white rounded")])

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
    [dash.dependencies.Output('graphique', 'figure'),
     dash.dependencies.Output('graphique-categories', 'figure'),
     dash.dependencies.Output('graphique-abstract', 'figure')],
    [dash.dependencies.Input('mot-recherche', 'value')])
def update_graph(mot_recherche):
    data = update_date(mot_recherche)

    # graphique avec plotly
    fig_keywords = px.line(data, x='Date', y='Count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche))
    fig_categories = px.histogram(data, x='Date', y='Count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche),color_discrete_sequence=['green'])
    fig_abstract = px.line(data, x='Date', y='Count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche),color_discrete_sequence=['red'])
                  
    total_occurrences = 0

    return fig_keywords, fig_categories, fig_abstract


def create_dashboard():
    app.run_server()


# lancé Dash avec Jup

