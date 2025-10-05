################################################ DIVVY BIKES DASHABOARD #####################################################
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from streamlit_keplergl import keplergl_static
import seaborn as sns
########################### Initial settings for the dashboard ##################################################################
st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("This dashboard aims to look at the potential reasons behind Citi Bike customers' complaints about bikes not being available at certain times.")
########################## Import data ###########################################################################################

df = pd.read_csv('NY_weather.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)
# ######################################### DEFINE THE CHARTS #####################################################################
## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color' : top20['value'], 'colorscale' : 'Blues'}))
fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width = True)

## Line chart 
fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', 
               marker={'color': 'blue'}),
    secondary_y = False
)

fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', 
               marker={'color': 'red'}),
    secondary_y=True
)

fig_2.update_layout(
    title_text="Daily Bike Rides and Temperature",
    xaxis_title="Date",
)

# Update y-axis titles (primary and secondary)
fig_2.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)  # Primary y-axis label
fig_2.update_yaxes(title_text="Temperature (°C)", secondary_y=True)  # Secondary y-axis label

st.plotly_chart(fig_2, use_container_width=True)
### Add the map  ###

path_to_html = "NY_dash.html"

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in Chicago")
st.components.v1.html(html_data,height=1000)