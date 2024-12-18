import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def getbowlsVisual(DF_deliveries,bowler):
    bowler_DF = DF_deliveries[~DF_deliveries['extras_type'].isin(['retired hurt','obstructing the field',
    'retired out'])]

    wicket_taker = bowler_DF.pivot_table(index='season',columns='bowler',aggfunc='sum',values='is_wicket',fill_value=0)
    wicket_taker.loc['total'] = wicket_taker.sum()
    wicket_taker = wicket_taker.sort_values(by='total',ascending=False,axis=1)
    wicket_taker.drop('total',inplace=True)
    wicket_taker.reset_index(inplace=True)

    fig1 = px.line(wicket_taker,x='season',y=bowler,line_shape='spline')

    fig1.update_layout(showlegend=False,title=dict(
                text=f"Wicket take by {bowler} over Season",
                x=0.5,
                y=0.95,
                font=dict(size=14, color='black',weight='bold'),
            ),
            plot_bgcolor='white',
            legend=dict(title= 'Bowlers',y=1,x=0.1,xanchor='center',yanchor='bottom'))

    fig1.update_xaxes(gridcolor='lightgrey')
    fig1.update_yaxes(gridcolor='lightgrey')


    CR = bowler_DF.pivot_table(
    index='season',
    values='total_runs',
    columns='bowler',
    aggfunc="sum"
    )

    wk = bowler_DF.pivot_table(
    index='season',
    values='is_wicket',
    columns='bowler',
    aggfunc="sum"
    )

    balls = bowler_DF.pivot_table(
    index='season',
    columns='bowler',
    values='total_runs',
    aggfunc='size'
    )

    bowlAvg = CR.div(wk)
    bowlAvg.loc['Total'] = bowlAvg.sum()
    bowlAvg.fillna(0)
    bowlAvg.replace([np.inf,-np.inf],0,inplace=True)
    bowlAvg = bowlAvg.sort_values(by='Total',ascending=False,axis=1)
    bowlAvg.drop('Total',inplace=True)
    bowlAvg.reset_index(inplace=True)
    fig2 = px.line(bowlAvg,x='season',y=bowler,line_shape='spline')

    fig2.update_layout(showlegend=False,title=dict(
                text=f"Bowling Average of {bowler} Over Seasons",
                x=0.5,
                y=0.95,
                font=dict(size=14, color='black',weight='bold'),
            ),
            plot_bgcolor='white')

    fig2.update_xaxes(gridcolor='lightgrey')
    fig2.update_yaxes(gridcolor='lightgrey')

    SRate = balls.div(wk)
    SRate.loc['Total'] = SRate.sum()
    SRate.fillna(0)
    SRate.replace([np.inf,-np.inf],0,inplace=True)
    SRate = SRate.sort_values(by='Total',ascending=False,axis=1)
    SRate.drop('Total',inplace=True)
    SRate.reset_index(inplace=True)
    fig3 = px.line(SRate,x='season',y=bowler,line_shape='spline')

    fig3.update_layout(showlegend=False,title=dict(
                text=f"Strick Rate of {bowler} Over Seasons",
                x=0.5,
                y=0.95,
                font=dict(size=14, color='black',weight='bold'),
            ),
            plot_bgcolor='white')

    fig3.update_xaxes(gridcolor='lightgrey')
    fig3.update_yaxes(gridcolor='lightgrey')
    
    ECO = CR.div(balls/6)
    ECO.loc['Total'] = ECO.sum()
    ECO.fillna(0)
    ECO.replace([np.inf,-np.inf],0,inplace=True)
    ECO = ECO.sort_values(by='Total',ascending=False,axis=1)
    ECO.drop('Total',inplace=True)
    ECO.reset_index(inplace=True)
    fig4 = px.line(ECO,x='season',y=bowler,line_shape='spline')

    fig4.update_layout(showlegend=False,title=dict(
                text=f"Economy of {bowler} Over Seasons",
                x=0.5,
                y=0.95,
                font=dict(size=14, color='black',weight='bold'),
            ),
            plot_bgcolor='white')

    fig4.update_xaxes(gridcolor='lightgrey')
    fig4.update_yaxes(gridcolor='lightgrey')


    legend_items = [{"label": trace.name, "color": trace.line.color} for trace in fig4.data]
    
    return fig1,fig2,fig3,fig4,legend_items

