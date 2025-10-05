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
DATA_CONFIG = {
    'chunk_size': 10000,  # Process data in chunks for better memory management
    'cache_timeout': 3600,  # Cache data for 1 hour to improve performance
    'max_memory_usage': '500MB'  # Prevent memory overflow
}
st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("This dashboard aims to look at the potential reasons behind Citi Bike customers' complaints about bikes not being available at certain times.")
########################## Import data ###########################################################################################

df = pd.read_csv('red.csv', index_col = 0)
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
fig_2,ax = plt.subplots(figsize=(10, 5))

sns.lineplot(data = df['bike_rides_daily'], color = "b")
ax.set_xlabel("Year 2022", fontsize = 14)
ax.set_ylabel("Bike rides daily", color = "navy", fontsize = 14)

ax2 = ax.twinx()

sns.lineplot(data = df["avgTemp"], color = "r", ax=ax2)
ax2.set_ylabel("Average temperatures", color = "red", fontsize=14)
plt.title('Temperature and trips in 2022', fontsize = 18)

st.plotly_chart(fig_2, use_container_width=True)
### Add the map  ###

path_to_html = "NY_dash.html"

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in Chicago")
st.components.v1.html(html_data,height=1000)