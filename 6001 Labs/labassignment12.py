import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc, html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

gss_summary1 = '''**The gender pay gap is the systemic difference in the median earnings between men and women, that persists despite wage discrimination based on sex having been made illegal in the 60s. The specific figure that the gender pay gap refers to is that on average women earn 82 cents for every dollar than men earn. This pay gap has remained steady for the past few decades despite increased equity in education and job occupation, and is exacerbated by other areas of discrimination such as race, ethnicity, and disability.**'''

gss_summary2 = '''**The General Study Survey, or GSS, is a biannual survey of the United States of America that measures both the demographic information of its participants as well as their opinions on a variety of social, political, and moral topics. The aim of GSS is to create a reliable source of long-term, comprehensive sociological data that can be used to understand the current social landscape of the United States, and how it has changed over time.**'''

sources = '''**https://www.americanprogress.org/article/quick-facts-gender-wage-gap/** 

**https://www.pewresearch.org/social-trends/2023/03/01/the-enduring-grip-of-the-gender-pay-gap/**

**https://www.pewresearch.org/short-reads/2023/03/01/gender-pay-gap-facts/**

**https://www.aauw.org/resources/research/simple-truth/**

**https://gss.norc.org/About-The-GSS**'''

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

gss_tab = gss_clean.groupby(['sex']).agg({'income':'mean',
                                           'job_prestige':'mean', 
                                           'socioeconomic_index': 'mean',
                                           'education': 'mean'}).reset_index().round(2)
gss_tab = gss_tab.rename(columns={'sex': 'Gender',
                                  'income':'Income',
                                  'job_prestige':'Occupational Prestige', 
                                  'socioeconomic_index': 'Socioeconomic Index',
                                  'education': 'Education'})
fig1 = go.Figure(data=[go.Table(
    header=dict(values=list(gss_tab.columns),
                fill_color='#4c78a8',
                font_color='white'),
    cells=dict(values=[gss_tab.Gender, gss_tab.Income, gss_tab['Occupational Prestige'], 
                       gss_tab['Socioeconomic Index'], gss_tab.Education],
               fill_color='#f58518'))
])

fig3 = px.scatter(gss_clean,
           y = 'income',
           x = 'job_prestige',
           color = 'sex',
           labels={'sex':'Gender',
                   'income':'Income', 
                   'job_prestige':'Occupational Prestige', 
                   'socioeconomic_index': 'Socioeconomic Index',
                   'education': 'Education'},
           hover_data = ["education", "socioeconomic_index"],
           trendline = 'ols',
           color_discrete_sequence=px.colors.qualitative.T10)

fig4 = px.box(gss_clean,
           x = 'income',
           y = 'sex',
           color = 'sex',
           labels={'income':'Income'},
           color_discrete_sequence=px.colors.qualitative.T10)
fig4.update_layout(showlegend = False)
fig4.update_yaxes(title = '')

fig5 = px.box(gss_clean,
           x = 'job_prestige',
           y = 'sex',
           color = 'sex',
           labels={'job_prestige':'Occupational Prestige'},
           color_discrete_sequence=px.colors.qualitative.T10)
fig5.update_layout(showlegend = False)
fig5.update_yaxes(title = '')

gss_abr = gss_clean[['income', 'sex', 'job_prestige']]
gss_abr['job_bins'] = pd.cut(gss_abr.job_prestige, bins=6, labels = [1,2,3,4,5,6])
gss_abr = gss_abr.dropna()
sex_categories = ['male', 'female']
gss_abr["sex"] = pd.Categorical(gss_abr["sex"], categories = sex_categories)
gss_abr = gss_abr.sort_values(by = ["sex", 'job_bins'])

fig6 = px.box(gss_abr, 
             x='income', 
             y='sex', 
             color='sex', 
             labels={'income':'Income'},
             facet_col='job_bins', 
             facet_col_wrap=2,
             color_discrete_sequence=px.colors.qualitative.T10)
fig6.update_layout(showlegend = False)
fig6.update_yaxes(title = '') 

app.layout = html.Div(
    [
        html.H1("GSS Gender Pay Gap Dashboard"),
        html.Div([
                    dcc.Tabs(
                        [dcc.Tab(label = 'About the gender wage gap', children = [
                            dcc.Markdown(children = gss_summary1)
                        ]),dcc.Tab(label = 'About the GSS', children = [
                            dcc.Markdown(children = gss_summary2)
                        ]),dcc.Tab(label = 'Sources', children = [
                            dcc.Markdown(children = sources)
                        ])]
                    )    
                ], style = {'width': '28%','float': 'left'}),
                html.Div([
                    dcc.Tabs(
                        [dcc.Tab(label = 'Data Table', children = [
                            html.H2("GSS Gender Data Average Table"),
                            dcc.Graph(figure=fig1)
                        ]),dcc.Tab(label = 'Opinions on Gender Roles', children = [
                            html.Div([
                                    html.Div([
                                    dcc.Markdown('Select a variable to display bars for:'),
                                    dcc.Dropdown(id = 'varselectx', 
                                                 options = gss_clean[['satjob','relationship','male_breadwinner',
                                                 'men_bettersuited','child_suffer','men_overwork']].columns,
                                                 value = 'male_breadwinner')
                                ], style={'width': '48%', 'float':'left'}),
                                html.Div([
                                    dcc.Markdown('Select a variable to group the bars by:'),
                                    dcc.Dropdown(id = 'varselecty', 
                                                 options = gss_clean[['sex','region','education']].columns,
                                                 value = 'sex')
                                ], style={'width': '48%', 'float':'right'})
                                ]),
                            html.Div([
                                html.H2("GSS Opinions on Gender Roles"),
                                dcc.Graph(id='bar')
                            ], style={'width':'100%', 'float':'left'})           
                        ]),dcc.Tab(label = 'Income vs Occupational Prestige', children = [
                            html.H2("GSS Income vs Occupational Prestige, by Gender"),
                            dcc.Graph(figure=fig3)                            
                        ]),dcc.Tab(label = 'Income/Job Prestige Distribution', children = [
                            html.Div([
                                        html.H2("GSS Income Distribution by Gender"),
                                        dcc.Graph(figure=fig4)
                                    ], style={'width': '48%', 'float':'left'}),
                            html.Div([
                                        html.H2("GSS Occupatinal Prestige Distribution by Gender"),
                                        dcc.Graph(figure=fig5)
                                    ], style={'width': '48%', 'float':'right'}),
                            html.H2("GSS Job Group Income Distribution by Gender"),
                            dcc.Graph(figure=fig6)
                        ])]
                    )           
                ], style = {'width': '68%','float': 'right'})
    ]
)

@app.callback(Output(component_id='bar',component_property='figure'),
              [Input(component_id='varselectx', component_property='value'),
               Input(component_id='varselecty', component_property='value')])

def barplot(xcol, ycol):
    gss_bar = gss_clean.groupby([ycol,xcol]).size().reset_index().rename({0: "Count"}, axis=1)
    fig2 = px.bar(gss_bar, x=ycol, y='Count', color=xcol,
                barmode = 'group',
                color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(showlegend=True)
    return fig2

if __name__=='__main__':
    app.run_server(debug=True, port=8050)