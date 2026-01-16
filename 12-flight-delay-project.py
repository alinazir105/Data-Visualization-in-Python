import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(
        'Flight Details Statistics Dashboard', 
        style={'textAlign':'center', 'color': '#503D36', 'font-size':35}
        ),
    html.Div([
        'Input Year', 
        dcc.Input(
            id='input-yr', 
            value='2010', 
            type='number', 
            style={'height':'35px', 'font-size': 35},
            ),
        ], style={'font-size': 40}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div(dcc.Graph(id='carrier-plot')),
        html.Div(dcc.Graph(id='weather-plot'))
    ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='nas-plot')),
        html.Div(dcc.Graph(id='security-plot'))
    ], style={'display': 'flex'}),
    html.Div(dcc.Graph(id='late-plot'),style={'width': '65%'})
])

def compute_info(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]

    carrier_delay_data = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    weather_delay_data = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    nas_delay_data = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    security_delay_data = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    late_delay_data = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return carrier_delay_data, weather_delay_data, nas_delay_data, security_delay_data, late_delay_data

@app.callback(
    [
        Output(component_id='carrier-plot', component_property='figure'),
        Output(component_id='weather-plot', component_property='figure'),
        Output(component_id='nas-plot', component_property='figure'),
        Output(component_id='security-plot', component_property='figure'),
        Output(component_id='late-plot', component_property='figure'),
    ], 
    Input(component_id='input-yr', component_property='value')
    )

def get_graphs(entered_year):
    carrier_delay_data, weather_delay_data, nas_delay_data, security_delay_data, late_delay_data = compute_info(airline_data, entered_year)

    # Line plot for Carrier Delay
    carrier_fig = px.line(
        carrier_delay_data,
        x='Month',
        y='CarrierDelay',
        color='Reporting_Airline',
        title='Month vs Carrier Delay Time',
        )
    
    # Line plot for Weather Delay
    weather_fig = px.line(
        weather_delay_data,
        x='Month',
        y='WeatherDelay',
        color='Reporting_Airline',
        title='Month vs Weather Delay Time',
        )
    
    # Line plot for NAS Delay
    nas_fig = px.line(
        nas_delay_data,
        x='Month',
        y='NASDelay',
        color='Reporting_Airline',
        title='Month vs NAS Delay Time',
        )
    
    # Line plot for Security Delay
    security_fig = px.line(
        security_delay_data,
        x='Month',
        y='SecurityDelay',
        color='Reporting_Airline',
        title='Month vs Security Delay Time',
        )
    
    # Line plot for Late Aircraft Delay
    late_fig = px.line(
        late_delay_data,
        x='Month',
        y='LateAircraftDelay',
        color='Reporting_Airline',
        title='Month vs Late Aircraft Delay Time',
        )
    return [carrier_fig, weather_fig, nas_fig, security_fig, late_fig]

if __name__ == '__main__':
    app.run()