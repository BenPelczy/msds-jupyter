import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import requests
import json
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

vacounties = pd.read_csv('vacounties.csv')
url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
r = requests.get(url)
counties = json.loads(r.text)
vacounties['county'] = [x.endswith('County') for x in vacounties['Jurisdiction']]
replace_map = {True: 'County',
               False: 'City'}
vacounties['county'] = vacounties['county'].replace(replace_map)
vacounties['income_to_col'] = vacounties['Average Annual Pay']/vacounties['Cost of living']

#Initialize Dashboard
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

#Populate Dashboard
app.layout = html.Div(
    [
        html.H1("Viriginia County Coast and Standard of Living Dashboard"),

        dcc.Tabs(
            [dcc.Tab(label = 'Statewide Data', children = [
                #statewide graphs here
                dcc.Markdown('Please select a variable:'),
                dcc.Dropdown(id = 'varselect', 
                             options = vacounties.columns, 
                             value = 'Average Annual Pay'), #Step 1: user input
                html.Div([
                    dcc.Graph(id='map'), #Step 5: display the output
                    dcc.Graph(id='boxplot')
                ], style = {'width': '58%','float': 'left'}),
                html.Div([
                    dcc.Graph(id='toptable')
                ], style = {'width': '38%','float': 'right'})
            ]), dcc.Tab(label = 'Data Relationships', children = [
                html.Div([
                    html.Div([
                    dcc.Markdown('Select a variable for the x-axis'),
                    dcc.Dropdown(id = 'varselectx', 
                                 options = vacounties.columns,
                                 value = 'Average Annual Pay')
                ], style={'width': '48%', 'float':'left'}), #dropdown1
                html.Div([
                    dcc.Markdown('Select a variable for the y-axis'),
                    dcc.Dropdown(id = 'varselecty', 
                                 options = vacounties.columns,
                                 value = 'Cost of living')
                ], style={'width': '48%', 'float':'right'})
                ]),
                html.Div([
                    dcc.Graph(id='scatter')
                ], style={'width':'100%', 'float':'left'})                
            ]), dcc.Tab(label = 'Data for One Locality', children = [
                #locality graphs here
                
            ])]
        )
    ]
)

@app.callback(Output(component_id='map',component_property='figure'), # Step 4: choose an id name for the return output
              [Input(component_id='varselect', component_property='value')]) #Step 2: pass input to callback

def makemap(col): #Step 3: pass the input to a function to generate the output
    fig = px.choropleth(vacounties, 
                        geojson = counties,
                        color = col,
                        scope = 'usa',
                        locations = 'FIPS',
                        hover_name = "Jurisdiction",
                        color_continuous_scale = 'greens',
                        hover_data = ['Total Population',
                                      'Average Annual Pay',
                                      'Cost of living',
                                     'Years of Potential Life Lost Rate',
                                     'Food Environment Index'])
    fig.update_geos(fitbounds='locations')
    return fig

@app.callback(Output(component_id='toptable',component_property='figure'),
              [Input(component_id='varselect', component_property='value')])

def maketable(col):
    dispdata = vacounties.sort_values(col, ascending=False)
    dispdata['Rank'] = list(range(1,dispdata.shape[0]+1))
    dispdata[col] = dispdata[col].astype('float').round(2)
    dispdata = dispdata[['Rank','Jurisdiction', col]]
    return ff.create_table(dispdata.head(15))

@app.callback(Output(component_id='boxplot',component_property='figure'),
              [Input(component_id='varselect', component_property='value')])

def makebox(col):
    fig = px.box(vacounties,
           x = col,
           y = 'county',
           hover_name = "Jurisdiction",
           color = 'county')
    fig.update_layout(showlegend = False)
    fig.update_yaxes(title = '')
    return fig

@app.callback(Output(component_id='scatter',component_property='figure'),
              [Input(component_id='varselectx', component_property='value'),
               Input(component_id='varselecty', component_property='value')])

def scatter(xcol, ycol):
    fig = px.scatter(vacounties,
           y = ycol,
           x = xcol,
           color = "Total Population",
           hover_name = "Jurisdiction",
           trendline = 'ols',
           width = 800,
           height = 800)
    return fig
    

#Run Dashboard
if __name__=='__main__':
    app.run_server(debug=True, port=8050)