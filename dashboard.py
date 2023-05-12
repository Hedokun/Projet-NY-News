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
liens = ["https://www.nytimes.com/2019/12/31/us/texas-church-shooting-white-settlement.html", "https://www.nytimes.com/2019/12/31/opinion/for-profit-college-veterans.html", "https://www.nytimes.com/2019/12/31/health/e-cigarettes-flavor-ban-trump.html", "https://www.nytimes.com/2019/12/31/crosswords/daily-puzzle-2020-01-01.html", "https://www.nytimes.com/2019/12/31/pageoneplus/corrections-jan-1-2020.html", "https://www.nytimes.com/2019/12/31/todayspaper/quotation-of-the-day-ex-seal-now-pitching-products-and-president.html", "https://www.nytimes.com/interactive/2019/12/31/world/middleeast/syria-united-nations-investigation.html", "https://www.nytimes.com/2020/01/01/world/asia/hong-kong-protest.html", "https://www.nytimes.com/2019/12/31/us/kevin-spacey-lawsuit-accuser.html", "https://www.nytimes.com/2019/12/31/us/politics/trump-new-years-eve.html"]
titre = ['Battling a Demon: Drifter Sought Help Before Texas Church Shooting', 'Protect Veterans From Fraud', 'F.D.A. Plans to Ban Most E-Cigarette Flavors but Menthol', 'It’s Green and Slimy', 'Corrections: Jan. 1, 2020', 'Quotation of the Day: Ex-SEAL Now Pitching Products and President', 'Hospitals and Schools Are Being Bombed in Syria. A U.N. Inquiry Is Limited. We Took a Deeper Look.', 'Hong Kong Protesters Return to Streets as New Year Begins', 'Kevin Spacey Accuser’s Estate Drops Sexual Assault Lawsuit', 'Dizzying Day for Trump Caps a Year Full of Them']
categories = ['U.S.', 'Opinion', 'Health', 'Crosswords & Games', 'Corrections', 'Today’s Paper', 'World', 'Science', 'Arts', 'Business Day', 'Magazine', 'Books', 'Well', 'Travel', 'Technology', 'New York', 'Movies', 'Real Estate', 'Sports', 'Theater', 'Food', 'Style', 'Parenting', 'Briefing', 'Climate', 'Smarter Living', 'Obituaries', 'The Learning Network', 'Reader Center', 'Podcasts', 'T Magazine', 'The Upshot', 'Fashion & Style', 'Your Money', 'Neediest Cases', 'Admin', 'T Brand', 'Video', 'The Weekly', 'Education', 'Automobiles', 'Sunday Review', 'Multimedia/Photos']

# créer une mise en page
app.layout = html.Div(children=[    
dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(href="#")),
    ],
    brand=html.Span("New-York Time Dashboard", className="font-roboto", style={'font-size': '36px', 'text-align': 'center',"font-weight": "bold"}),
    brand_href="#",
    color="#0D75FA",
    dark=True,
    links_left = True,
    class_name='mb-3'
),
    dbc.Row([
            dbc.Card(             
                dbc.Row(children = [
                    dbc.Col(dbc.Input(id='mot-recherche',placeholder="Entrez le mot à rechercher", type="text"),width=2,className="mb-2 rounded"),
                    dbc.Col(dcc.Dropdown(id='dropdown-categories', options=[{'label': category, 'value': category} for category in categories],style={'width': '60%'} , placeholder="Sélectionnez une catégorie")),
                    dbc.Col(dcc.DatePickerRange(id='my-date-picker-range', min_date_allowed=date(1995, 8, 5), max_date_allowed=date(2023, 5, 11),initial_visible_month=date(2017, 8, 5), end_date=date(2017, 8, 25),className= "rounded"))
                    
        ]),className="rounded shadow-sm p-4"),  
    ],className="p-3"),

dbc.Row([
        #graph 1 categories
    dbc.Col(
        dbc.Card(
            dbc.CardBody(children=[dcc.Graph(id='graphique-categories')]),
            className="shadow bg-white rounded"
        ),
        width=7,
        className='p-3'
            ),
        #tableau 1 liens
            dbc.Col(
                html.Table([
                    html.Thead(html.Tr([html.Th("Liens")]), style={'background-color': '#f8f9fa'}),
                    html.Tbody([html.Tr([html.Td(html.A(href=lien, children=lien))]) for lien in liens])
                ], className="table")
                , width=4)

        ], className="mb-3"),

        #graph 2 abstract
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(children=[dcc.Graph(id='graphique-abstract')]),
                    className="shadow bg-white rounded"
                ),
                width=7),
        #tableau 2 Titres
            dbc.Col(
                html.Table([
                    html.Thead(html.Tr([html.Th("Titres")]), style={'background-color': '#f8f9fa'}),
                    html.Tbody([html.Tr([html.Td(element)]) for element in titre])
                ], className="table")
                , width=4)
        ], className="p-3")
    
])




try :
    es = connect_elastic_server()
except :
    es = 0

def update_date(filter):
    try :
        date, count = get_count_article_range2(es, filter)
        d = {'Date': date, 'Count': count}
    except :
        d = {'Date': "20/01/2001", 'Count': 25}

    df = pd.DataFrame(d)
    print(df)
    return df


# definir une fonction de rappel pour mettre à jour le graphique en fonction du mot de recherche
@app.callback(
    [dash.dependencies.Output('graphique', 'figure'),
     dash.dependencies.Output('graphique-categories', 'figure'),
     dash.dependencies.Output('dropdown-output', 'children'),
     dash.dependencies.Output('graphique-abstract', 'figure')],
    [dash.dependencies.Input('mot-recherche', 'value'),
     dash.dependencies.Input('dropdown-categories', 'value')])

#update du choix de catagory
def display_category(selected_category):
    if selected_category:
        return html.H3(f"Vous avez sélectionné la catégorie : {selected_category}")
    else:
        return html.H3("Sélectionnez une catégorie")
    


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




