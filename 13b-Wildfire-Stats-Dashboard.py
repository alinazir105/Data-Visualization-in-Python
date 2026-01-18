import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import datetime as dt

app = dash.Dash(__name__)

wildfire_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

wildfire_data['Year'] = pd.to_datetime(wildfire_data['Date']).dt.year
wildfire_data['Month'] = pd.to_datetime(wildfire_data['Date']).dt.month_name()

# center aligned, with color code #503D36, and font-size as 26
app.layout = html.Div(children=[
    html.H1(
        'Austrailia Wildfire Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}
    ),
    html.Div([   
        html.H2('Select Region:', style={'margin-right': '2em'}), 
        dcc.RadioItems(
            options=[
                {'label':'New South Wales', 'value':'NSW'},
                {'label':'Northern Territory', 'value':'NT'},
                {'label':'Queensland', 'value':'QL'},
                {'label':'South Austrailia', 'value':'SA'},
                {'label':'Tasmania', 'value':'TA'},
                {'label':'Victoria', 'value':'VI'},
                {'label':'Western Austrailia', 'value':'WA'},
        ], value='NSW', id='region', inline=True
        )
    ]),
    html.Div([
        html.H2('Select Year:', style={'margin-right': '2em'}),
        dcc.Dropdown(wildfire_data.Year.unique(), value=2005, id='year')
    ]),
    html.Div([
        html.Div(dcc.Graph(id='plot1'), style={'width':'50%'}),
        html.Div(dcc.Graph(id='plot2'), style={'width':'50%'})
    ], style={'display': 'flex'})
])

@app.callback(
    [
        Output(component_id='plot1', component_property='figure'),
        Output(component_id='plot2', component_property='figure')
    ],
    [
        Input(component_id='region', component_property='value'),
        Input(component_id='year', component_property='value')
    ])

def get_graphs(region, year):
    region_data = wildfire_data[wildfire_data['Region'] == region]
    year_data = region_data[region_data['Year'] == int(year)]
    
    #Pie chart
    avg_monthly_fire_data = year_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    montly_region_pie_chart = px.pie(avg_monthly_fire_data, values='Estimated_fire_area', names='Month', title=f'{region}: Monthly Average Estimated Fire Area in year {year}')
    
    #Bar chart
    avg_pixel_count_data = year_data.groupby('Month')['Count'].sum().reset_index()
    monthly_region_bar_chart = px.bar(avg_pixel_count_data, x='Month', y='Count', title=f'{region}: Average Count of Pixels for Presumed Vegetation Fires in year {year}')

    return montly_region_pie_chart, monthly_region_bar_chart

if __name__ == '__main__':
    app.run()