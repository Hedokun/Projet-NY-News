import json

import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import *
import dash_table
import requests


url_api = "http://127.0.0.1:8000/"


def get_all_data():
    response = requests.get(url_api + f"get_time_bdd/")
    reponse_get_time_bdd = json.loads(response.content.decode())

    response = requests.get(url_api + f"get_last_news/")
    reponse_get_last_news = json.loads(response.content.decode())

    response = requests.get(url_api + f"get_top10/")
    reponse_get_top10 = json.loads(response.content.decode())


    return reponse_get_top10, reponse_get_last_news, reponse_get_time_bdd

reponse_get_top10, reponse_get_last_news, reponse_get_time_bdd = get_all_data()

min_datetime = datetime.strptime(reponse_get_time_bdd["min_time"], "%Y-%m-%dT%H:%M:%S")

max_datetime = datetime.strptime(reponse_get_time_bdd["max_time"], "%Y-%m-%dT%H:%M:%S")



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


logo = html.Img(src="https://i0.wp.com/datascientest.com/wp-content/uploads/2020/08/new-logo.png", height="70px", 
                 className="position-absolute top-0 end-60")   
# titre
header = dbc.NavbarSimple(
    children = [
        dbc.NavItem(dbc.NavLink(href="#")),
    ],
    brand = html.Div([
        html.Span(" New-York Time Dashboard", className="font-roboto", style={'font-size': '36px', 'text-align': 'center',"font-weight": "bold"})
        ]),
    brand_href="#",
    color="#472ADE",
    dark=True,
    links_left = True,
    class_name='mb-3'
)
footer = html.Footer(
    dbc.Container(
        dbc.Row(
            dbc.Col(
                html.P("Ce projet c'est fait dans le cadre de la formation Datascientest par Alexis Peron, Edouard Loiseau, Louis Petat Lenoir."),
                style={'text-align': 'center'}
            )
        ),
        fluid=True
    ),
    className="footer py-3 mt-5 bg-light"
)

recherche = dbc.Col(dbc.Input
                            (id='mot-recherche',placeholder="Entrez le mot à rechercher", type="text"),width=4,className="mb-2 rounded")
Dropdown = dbc.Col(dcc.Dropdown
                            (id='dropdown_categories', options=[{'label': category, 'value': category} for category in reponse_get_top10["Keyword"]],style={'width': '60%'},className= "mb-2 rounded" , placeholder="Sélectionnez une catégorie"))
picker = dbc.Col(dcc.DatePickerRange
                            (id='my_date_picker_range', min_date_allowed=min_datetime, max_date_allowed=max_datetime,initial_visible_month=min_datetime,className= "mb-2 rounded"))

 
# bouton: mot de recherche, sélection catégorie, date
selector =dbc.Row([
            dbc.Card(             
                dbc.Row(children = [picker
                
        ],className="flex-column"),className="rounded shadow-sm p-4"),  
    ],className="p-3")

picker = dbc.Col(dcc.DatePickerRange(id='my_date_picker_range', min_date_allowed=min_datetime,
                                     max_date_allowed=max_datetime, initial_visible_month=min_datetime, className="mb-2 rounded"))

# bouton: mot de recherche, sélection catégorie, date
selector = dbc.Row([
    dbc.Col(dbc.Card(dbc.Row(children=[picker]), className="flex-column"), className="rounded shadow-sm p-4"),
], className="p-3")
        
#tableau 1 titres et liens
tab_Titres = dbc.Col(
    dbc.Table(
        [
            html.Thead(
                html.Tr([html.Th("Latest News")]),
                style={"background-color": "#f8f9fa"}
            ),
            html.Tbody([
                    html.Tr([
                            html.Td(html.A(t,href=lien,target="_blank",)),
                            ])
                    for t, lien in zip(reponse_get_last_news["Title"], reponse_get_last_news["Url"])
                    ]),
        ],
        bordered=True,
        responsive=True,
        hover=True,
        striped=True
    ),
)
#graph 1 categories
graph_1 =  dbc.Tab(
    label="Tendance de la recherche",
    children=[recherche,
        dbc.Card(
            dbc.CardBody(dcc.Graph(id='graphique-1')),className="shadow bg-white rounded")
    ]
)
#graph 2 abstract
graph_2 = dbc.Tab(
    label="Tendance par thematique d'article",
    children=[Dropdown,
        dbc.Card(
            dbc.CardBody(dcc.Graph(id='graphique-2')),className="shadow bg-white rounded")
    ]
)

tabs = dbc.Tabs(
    [graph_1, graph_2],
    className="mb-3"
)


# créer une mise en page
app.layout = html.Div(children=[  
        header,
        logo, 
        dbc.Row([
        dbc.Col(selector,width=2, className="p-2"),        
        dbc.Col(tabs, className="p-3"),
        dbc.Col(tab_Titres,width=3, className="p-4"),
        footer
        ])

])


def update_data_article(filter,min_date,max_date):
    response = requests.get(url_api+f"get_count_article/?param={filter}&min_date={min_date}&max_date={max_date}")
    reponse_parse = json.loads(response.content.decode())
    df = pd.DataFrame(reponse_parse)
    return df

def updata_data_catagories(filter):
    response = requests.get(url_api + f"get_cat_by_day/?param={filter}")
    response_get_cat_by_day = json.loads(response.content.decode())
    df = pd.DataFrame(response_get_cat_by_day)
    return df



def display_category(selected_category):
    if selected_category:
        return html.H3(f"Vous avez sélectionné la catégorie : {selected_category}")
    else:
        return html.H3("Sélectionnez une catégorie")


# definir une fonction de rappel pour mettre à jour le graphique en fonction du mot de recherche
@app.callback(
    [dash.dependencies.Output('graphique-1', 'figure'),
     dash.dependencies.Output('graphique-2', 'figure')],
    [dash.dependencies.Input('mot-recherche', 'value'),
     dash.dependencies.Input('dropdown_categories', 'value'),
     dash.dependencies.Input('my_date_picker_range', 'start_date'),
    dash.dependencies.Input('my_date_picker_range', 'end_date')])
#update du choix de catagory
def update_graph(mot_recherche,dropdown_categories, start_date,end_date):
    if mot_recherche== None :
        mot_recherche = "France"
    data_article = update_data_article(mot_recherche,start_date,end_date)
    data_categories = updata_data_catagories(dropdown_categories)
    display_category(dropdown_categories)
    # graphique avec plotly
    fig_keywords = px.line(data_article, x='Date', y='Count',
                  title='Nombre d\'articles contenant le mot "{}"'.format(mot_recherche))
    fig_categories = px.line(data_categories, x='Date', y='Count',
                  title='Nombre d\'articles de la catégorie "{}"'.format(dropdown_categories),color_discrete_sequence=['green'])
    #fig_abstract = px.line(data, x='Date', y='Count',
                  #title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche),color_discrete_sequence=['red'])
                  
    total_occurrences = 0

    return fig_keywords, fig_categories #fig_abstract


def create_dashboard():
    app.run_server()



# lancé Dash avec Jup
create_dashboard()

