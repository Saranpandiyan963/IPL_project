import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def getbatsVisual(DF_deliveries,player):
    BatsmanScore = DF_deliveries.pivot_table(index=['season'],columns='batter',values='batsman_runs',aggfunc='sum',fill_value=0)
    BatsmanScore.loc['Total'] = BatsmanScore.sum()
    BatsmanScore = BatsmanScore.sort_values(by='Total',ascending=False,axis=1)
    BatsmanScore.drop('Total',inplace=True)
    BatsmanScore = BatsmanScore.reset_index()

    fig1 = px.line(BatsmanScore,x='season',y=player,line_shape='spline')

    Text = 'Runs of Batsman over Season'

    fig1.update_layout(showlegend=True,title=dict(
            text=Text,
            x=0.5,
            y=0.95, 
            font=dict(size=14, color='black',weight='bold'),
        ),
        plot_bgcolor='white')

    fig1.update_xaxes(gridcolor='lightgrey')
    fig1.update_yaxes(gridcolor='lightgrey')



    BatsmanScore = DF_deliveries.pivot_table(index=['season'],columns='batter',values='batsman_runs',aggfunc='sum',fill_value=0)
    DismisalPiv = DF_deliveries.pivot_table(index=['season'],columns='batter',values='player_dismissed',aggfunc='count',fill_value=0)

    batAve = BatsmanScore.div(DismisalPiv)

    batAve.replace([np.inf, -np.inf], 0, inplace=True)
    batAve.fillna(0,axis=1,inplace=True)
    batAve.loc['Total'] = batAve.sum()
    batAve = batAve.sort_values(by='Total',ascending=False,axis=1)
    batAve.drop('Total',inplace=True)
    batAve = batAve.reset_index()

    fig2 = px.line(batAve.reset_index(),x='season',y=player,line_shape='spline')

    fig2.update_layout(showlegend=False,title=dict(
                text=f"Batting Average of {player}",
                x=0.5,
                y=0.95,
                font=dict(size=14, color='black',weight='bold'),
            ),
            plot_bgcolor='white')

    fig2.update_xaxes(gridcolor='lightgrey')
    fig2.update_yaxes(gridcolor='lightgrey')


    BatsmanScore = DF_deliveries.pivot_table(index=['season'],columns='batter',values='batsman_runs',aggfunc='sum',fill_value=0)
    condition = ((DF_deliveries['extras_type'].isin(['legbyes','noballs'])) | (pd.isna(DF_deliveries['extras_type'])))

    ballFaced = DF_deliveries[condition].pivot_table(index=['season'],columns='batter',values='total_runs',aggfunc='count',fill_value=0)
    StrickRate_DF = BatsmanScore.div(ballFaced/100)

    StrickRate_DF.replace([np.inf, -np.inf], 0, inplace=True)
    StrickRate_DF.fillna(0,axis=1,inplace=True)
    StrickRate_DF.loc['Total'] = StrickRate_DF.sum()
    StrickRate_DF = StrickRate_DF.sort_values(by='Total',ascending=False,axis=1)
    StrickRate_DF.drop('Total',inplace=True)
    StrickRate_DF = StrickRate_DF.reset_index()
    StrickRate_DF = StrickRate_DF.set_index('season')

    fig3 = px.line(StrickRate_DF.reset_index(),x='season',y=player,line_shape='spline')

    fig3.update_layout(showlegend=False,title=dict(
                text=f"Strick Rate of {player}",
                x=0.5,
                y=0.95,
                font=dict(size=14, color='black',weight='bold'),
            ),
            plot_bgcolor='white')

    fig3.update_xaxes(gridcolor='lightgrey')
    fig3.update_yaxes(gridcolor='lightgrey')

    legend_items = [{"label": trace.name, "color": trace.line.color} for trace in fig1.data]
    return fig1,fig2,fig3,legend_items