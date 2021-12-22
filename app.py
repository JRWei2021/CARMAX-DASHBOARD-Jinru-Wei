# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 07:59:57 2021

@author: Jinru
"""

"""
Dashboard starter template
"""

import dash
import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from dash import no_update
import plotly.graph_objects as go
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']






# original data
df = pd.read_csv("carmax2.csv")
df_im = df

# data for bar chart
df_year = df.groupby('Year').agg('count').reset_index()
df_year = df_year.loc[:,['Year', 'Type']]
df_year.columns = ['Year','Inventory']

fig = px.bar(df_year, x='Year', y="Inventory", color="Inventory", barmode="group", title='Current Inventory in CARMAX')


#data for scatterplot 1

df_im['Make_Model'] = df['Make'] + " " + df['Model'] 


df_im['Price'] = df_im['Price'].str.replace('$','')
df_im['Price'] = df_im['Price'].str.replace(',','')
df_im['Milleage'] = df_im['Milleage'].str.replace('K mi','000')

df_im['Price'] = pd.to_numeric(df_im['Price'])
df_im['Milleage'] = pd.to_numeric(df_im['Milleage'])
df_im['Year'] = pd.to_numeric(df_im['Year'])
df_im['Average Review'] = pd.to_numeric(df_im['Average Review'])



fig_im = go.Figure(data=[
    go.Scatter(
        x=df_im["Milleage"],
        y=df_im["Price"],
        mode="markers",
        marker=dict(
            colorscale='viridis',
            color=df_im["Year"],
            colorbar={"title": "Year"},
            line={"color": "#444"},
            reversescale=True,
            sizeref=45,
            sizemode="diameter",
            opacity=0.8,
            
        )
    )
])

# turn off native plotly.js hover effects - make sure to use
# hoverinfo="none" rather than "skip" which also halts events.
fig_im.update_traces(hoverinfo="none", hovertemplate=None)

fig_im.update_layout(
    xaxis=dict(title='Milleage (miles)'),
    yaxis=dict(title='Price (dollars)'),
    plot_bgcolor='rgba(255,255,255,0.1)'
)



# data for scatter plot 2
df1 = df.loc[:,['Year', 'Price','Milleage','Average Review']]
df1.columns = ['Year', 'Price', 'Milleage','Average Review']
sc_varible = df1.columns.tolist()
sc_varible = np.array(sc_varible)


df_sc = df.loc[:,['Year', 'Price','Milleage','Average Review','Transmission','Make','Model','Type']]
df_sc['Make_Model'] = df['Make'] + " " + df['Model']
del df_sc['Model']
del df_sc['Make']

#df_sc['Price'] = df_sc['Price'].str.replace('$','')
#df_sc['Price'] = df_sc['Price'].str.replace(',','')
#df_sc['Milleage'] = df_sc['Milleage'].str.replace('K mi','000')

df_sc['Price'] = pd.to_numeric(df_sc['Price'])
df_sc['Milleage'] = pd.to_numeric(df_sc['Milleage'])
df_sc['Year'] = pd.to_numeric(df_sc['Year'])
df_sc['Average Review'] = pd.to_numeric(df_sc['Average Review'])


markdown_text = '''
#### Data Resource: [CARMAX](https://www.carmax.com/cars)    
####    MA 705 Data Science 
####    December 2021, Jinru Wei
'''

markdown_text2 = '''

### About this Dashboard
#### The dataset we used were collected from [CARMAX](https://www.carmax.com/cars) 
#### You can get to all the inventory information through following graphs:
##### 1. Check the specific inventory for each year.
##### 2. View the detailed descriptions and picture of each car by moving your cursor.  
##### 3. Customize a comparion among all the cars.
##### 4. Explore the entire dataset by simply searching, sorting, or deleting anything you want. 
'''


app = dash.Dash(__name__, external_stylesheets=stylesheet)

app.layout = html.Div([
    html.H1(
        "CARMAX Inventory Dashboard",
            style={'textAlign': 'center'}
            ),
    
    html.Hr(),
    
          dcc.Markdown(children=markdown_text2,style={'width': '50%', 'display': 'inline-block', 'float': 'left'}),
            
        html.Div([ 
            dcc.Graph(
                id='example-graph',
                figure=fig,
                style={'width': '50%', 'display': 'inline-block', 'float': 'right'}),

     
    
    dcc.Graph(id="graph-basic-2", figure=fig_im, clear_on_unhover=True,
              style={'width': '80%', 'display': 'inline-block',"padding-top": "10px",
                            "padding-left": "150px"}),
    dcc.Tooltip(id="graph-tooltip"),
    
    
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in sc_varible],
                value='Year'
            ),
         
        ], style={'width': '20%', 'display': 'inline-block', 'float' : 'left',"padding-left": "200px"}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in sc_varible],
                value='Price'
            ),
            
        ], style={'width': '20%', 'float': 'right', 'display': 'inline-block',"padding-right": "300px"})
    ]),

    dcc.Graph(id='indicator-graphic', style={'width': '80%', 'display': 'inline-block',
                            "padding-left": "150px"}),
 

    html.Div(  
      dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 15
        ),
      style={'width': '80%', 'overflowY': 'scroll', "padding-top": "10px",
                            "padding-left": "150px"}
      ),
      
      html.Div(id='datatable-interactivity-container'),
      
      html.Hr(),
      
      dcc.Markdown(children=markdown_text)
        ])
      ])
            
server = app.server

@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("graph-basic-2", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df_im.iloc[num]
    img_src = df_row['Car Image']
    name = df_row['Make']
    form = df_row['Model']
    desc = df_row['Description']
    avai = df_row['Availability']
    if len(desc) > 300:
        desc = desc[:100] + '...'

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{name}", style={"color": "darkblue"}),
            html.P(f"{form}"),
            html.P(f"{desc}"),
            html.P(f"{avai}"),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]

    return True, bbox, children         





@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 400,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
    ]

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))

def update_graph(xaxis_column_name, yaxis_column_name
                 ):

    
    fig = px.scatter(x=df_sc[xaxis_column_name],
                     y=df_sc[yaxis_column_name],
                     color = df_sc['Type'],
                     hover_name=(df_sc['Make_Model']),
        )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    
    fig.update_xaxes(title=xaxis_column_name)

    fig.update_yaxes(title=yaxis_column_name)

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    

