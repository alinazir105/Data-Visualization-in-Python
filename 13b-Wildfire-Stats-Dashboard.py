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
    )
])

if __name__ == '__main__':
    app.run()