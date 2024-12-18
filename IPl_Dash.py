from dash import html,Dash,dcc,callback,Output,Input
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pickle

from src.dash1 import gen_visual as gen_visual_1
from src.dash1 import gen_visual2 as gen_visual_2
from src.dashBat import getbatsVisual as genbatsVisuals
from src.dashBowl import getbowlsVisual as genbowlVisuals

with open('Df_matches.pkl', 'rb') as file:
    Df_matches = pickle.load(file)

with open('Df_deliveries.pkl', 'rb') as file:
    DF_deliveries = pickle.load(file)

# DF_deliveries['season'] = DF_deliveries['match_id'].map(Df_matches.set_index('id')['season'])

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME], title='IPL Dash Board')

app.config.suppress_callback_exceptions = True

Df_matches_league = Df_matches[Df_matches['match_type'] == 'League']
match_pivot=Df_matches_league.pivot_table(columns='winner',index='season',aggfunc='size',fill_value=0)
match_pivot.loc['Total'] = match_pivot.sum()
match_pivot = match_pivot[match_pivot.loc['Total'].sort_values(ascending=False).index]
match_pivot.drop('Total',inplace=True)
match_pivot = match_pivot.div(14/100)
plotable = match_pivot
plotable = plotable.reset_index()



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
        dbc.NavItem(dbc.NavLink("Team Performance", href="/",id="nav-link-1",style={"font-size": "18px"})),
        dbc.NavItem(dbc.NavLink("Player Performance", href="/Player", id="nav-link-2",style={"font-size": "18px"}))
    ],
    brand=html.Div(
        [
            html.Img(src="assets/logo.webp", height="40px", style={"margin-right": "10px"}),
            "IPL Performance Dashboard",
        ],
        style={"display": "flex", "align-items": "center"},
    ),
    brand_href="#",
    color="#19388A",
    dark=True,
    style={"font-weight": "bold", "font-size": "24px"}),
    dcc.Loading([html.Div(id='page-content')],type='default',color='#F9CD05',overlay_style={"visibility":"visible", "filter": "blur(2px)"}),
    html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.A(
                    html.Img(src="assets/icons8-github-100.png", alt="GitHub", style={"height": "30px", "margin-right": "15px"}),
                    href="https://github.com/your-profile", target="_blank"
                ),
                html.A(
                    html.Img(src="assets/icons8-linkedin-logo-100.png", alt="LinkedIn", style={"height": "30px", "margin-right": "15px"}),
                    href="https://www.linkedin.com/in/saran-pandiyan-b-6b033521b/", target="_blank"
                ),
                html.A(
                    html.Img(src="assets/icons8-gmail-100.png", alt="Gmail", style={"height": "30px"}),
                    href="mailto:pandiyansaran7@gmail.com"
                )
            ], md=12, className="text-center")
        ]),
        dbc.Row([
            dbc.Col(html.P("Thanks for visiting!", style={"margin-top": "10px", "font-size": "14px"}), className="text-center")
        ])
    ], fluid=True, style={
        "background-color": "#19388A",
        "color": "white",  
        "padding": "20px 0",  
        "margin-top": "auto" 
    })
])

])

@callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
)

def display_page(pathname):

    if pathname == '/':

        return dbc.Container([
        dbc.Row([
                dcc.Dropdown(
                options=[{"label": col, "value": col} for col in plotable.columns],
                value="Mumbai Indians",
                multi=True,
                id="dropdown",
                style={'color':'black','padding':'10px'}
            )
            ]),
            dbc.Row([dcc.Graph(id="graph")]),
            dbc.Row([html.H4("Please select The Desired Team Name",style={
            "text-align": "left",  
            "margin-top": "20px",  
            "margin-bottom": "0px",  
            "display": "flex",  
            "align-items": "center",  
        })]),
            dbc.Row([
                dcc.Dropdown(
                options=[{"label": col, "value": col} for col in plotable.columns],
                value="Mumbai Indians",
                multi=False,
                id="dropdown2",
                style={'color':'black','padding':'10px'}
            )
            ]),
            dbc.Row([
            dcc.Graph(id="graph2")]),
            dbc.Row([
            dcc.Graph(id="graph3")])
    ],style={'padding': '10px'},id='page-content')

    elif pathname == '/Player':

        return dbc.Container([

            dbc.Row([html.H4("Please Select Batsman from dropdown",style={
            "text-align": "left",  
            "margin-top": "20px",  
            "margin-bottom": "0px",  
            "display": "flex",  
            "align-items": "center",  
        })]),

            dbc.Row([
                dcc.Dropdown(
                options=[{"label": col, "value": col} for col in DF_deliveries['batter'].unique()],
                value="MS Dhoni",
                multi=True,
                id="batterDropdown",
                style={'color':'black','padding':'10px'}
            )
            ]),
            dbc.Row([html.Div(id='LegendBatter')]),
            dbc.Row([
                dcc.Graph(id="graphBat")
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="graphAvg"),width=6),
                dbc.Col(dcc.Graph(id="graphSR"),width=6)
            ],style={"margin-top": "20px"}),

            dbc.Row([html.H4("Please Select Bowlers from dropdown",style={
            "text-align": "left",  
            "margin-top": "20px",  
            "margin-bottom": "0px",  
            "display": "flex",  
            "align-items": "center",  
        })]),

            dbc.Row([
                dcc.Dropdown(
                options=[{"label": col, "value": col} for col in DF_deliveries['bowler'].unique()],
                value="YS Chahal",
                multi=True,
                id="BowlerDropdown",
                style={'color':'black','padding':'10px'}
            ),
            ]),
            dbc.Row([html.Div(id='bowllegend')]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="graphwkt"),width=6),
                dbc.Col(dcc.Graph(id="graphECO"),width=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="graphBowlAvg"),width=6),
                dbc.Col(dcc.Graph(id="graphBowlSR"),width=6),
            ],style={"margin-top": "20px"})
        ])

    else:

        return html.P('404 Not Found')

@callback(
        Output("graphBat","figure"),
        Output("graphAvg","figure"),
        Output("graphSR","figure"),
        Output("LegendBatter","children"),
        Input("batterDropdown","value")
)

def updateBatter(batter):
    fig1,fig2,fig3,legend_items= genbatsVisuals(DF_deliveries,batter)

    ledgend = [html.Span([
                    html.Span(style={'backgroundColor': item["color"],
                                     'display': 'inline-block',
                                     'width': '20px',
                                     'height': '20px',
                                     'margin-right': '10px'}),
                    html.Span(item["label"])
                ], style={"margin-right": "10px"}) for item in legend_items]

    return fig1,fig2,fig3,ledgend


@callback(
        Output("graphwkt","figure"),
        Output("graphECO","figure"),
        Output("graphBowlAvg","figure"),
        Output("graphBowlSR","figure"),
        Output('bowllegend', 'children'),
        Input("BowlerDropdown","value")
)

def UpdateBowler(bowl):
    fig1,fig2,fig3,fig4,legend_items = genbowlVisuals(DF_deliveries,bowl)

    ledgend = [html.Span([
                    html.Span(style={'backgroundColor': item["color"],
                                     'display': 'inline-block',
                                     'width': '20px',
                                     'height': '20px',
                                     'margin-right': '10px'}),
                    html.Span(item["label"])
                ], style={"margin-right": "10px"}) for item in legend_items]

    return fig1,fig2,fig3,fig4,ledgend



@callback(
    Output("graph","figure"),
    Input("dropdown","value")
)

def update_graph(val):
    
    fig = px.line(plotable,
              x='season',
              y=val,
              line_shape='spline',
              labels={'season':'Seasons (Years)','value':'Match winning in %'}
              )

    Title = 'Team Performance in league'

    fig.update_layout(showlegend=True,title=dict(
                    text=Title,
                    x=0.5,
                    y=0.95,
                    font=dict(size=20, color='black',weight='bold'),
                ),
                plot_bgcolor='white')


    fig.update_xaxes(gridcolor='lightgrey')
    fig.update_yaxes(gridcolor='lightgrey')

    return fig

@callback(
    Output('graph2','figure'),
    Output('graph3','figure'),
    Input('dropdown2','value')
)

def update_graph2(val):
    return gen_visual_1(Df_matches,val),gen_visual_2(Df_matches,val)

# add for stying purpose only
@callback(
    [Output("nav-link-1", "active"), Output("nav-link-2", "active")],
    Input("url", "pathname")
)
def update_active_links(pathname):
    return pathname == "/", pathname == "/Player"

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)


