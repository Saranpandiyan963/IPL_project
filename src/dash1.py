import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

def get_matchwin(Df,team1):

    Df = Df[(Df['team1'] == team1) | (Df['team2'] == team1)]

    opponents = set(Df['team1'].tolist() + Df['team2'].tolist())
    opponents.discard(team1)

    result = []

    for opponent in opponents:
        matchwin = Df[((Df['team1'] == team1) & (Df['team2'] == opponent)) | ((Df['team1'] == opponent) & (Df['team2'] == team1))]

        winlist = matchwin['winner'].value_counts().to_dict()
        
        result.append({'Team': team1 , 'Opponent': opponent, 'Wins': winlist.get(team1,0), 'Opponent Wins': winlist.get(opponent,0)})

    return pd.DataFrame(result)


def gen_visual(Df_vs,Team):
    
    Df_vs = get_matchwin(Df_vs,Team)
    Df_vs['Team win Percentage'] = Df_vs['Wins']/(Df_vs['Wins'] + Df_vs['Opponent Wins'])*100
    Df_vs['Opponent win Percentage'] = Df_vs['Opponent Wins']/(Df_vs['Wins'] + Df_vs['Opponent Wins'])*100
    Df_vs = Df_vs.sort_values(by='Team win Percentage',ascending=True)

    fig = px.bar(Df_vs,x=['Team win Percentage','Opponent win Percentage'], y='Opponent',text_auto='0.2s',labels={'Opponent':'Opponent Teams','value':f'{Team} Win Ratio in % '},
             hover_data=['Wins','Opponent Wins'])
    fig.update_layout(plot_bgcolor="white",yaxis=dict(side='right'),legend=dict(title=f'{Team} Win Distribution',y=1,x=0.1,xanchor='center',yanchor='bottom'), title=dict(text=Team,x=0.5,y=0.95,font=dict(weight='bold')))
    fig.update_traces(textposition='inside')
    return fig

def gen_visual2(Df_matches,Team):

    Df_mat = Df_matches[(Df_matches['team1'] == Team) | (Df_matches['team2'] == Team)].copy()
    Df_Runs= Df_mat[Df_matches['result'] ==  'runs'].copy() # runs wickets
    Df_Wickets= Df_mat[Df_matches['result'] ==  'wickets'].copy()

    fig = make_subplots(rows=2,cols=2,
    specs=[[{'colspan':2},None],
           [{},{}]],
    subplot_titles=('Target Plot Distribution','Result Margin by Wicket Distribution','Result Margin by Run Distribution')
    )

    fig.add_trace(go.Histogram(x=Df_mat['target_runs'],nbinsx=25),row=1,col=1)
    fig.add_trace(go.Histogram(x=Df_Wickets['result_margin'],nbinsx=25),row=2,col=1)
    fig.add_trace(go.Histogram(x=Df_Runs['result_margin'],nbinsx=50),row=2,col=2)

    fig.update_layout(showlegend=False,height=600,plot_bgcolor='white')
    return fig
