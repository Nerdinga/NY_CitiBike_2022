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
from PIL import Image
from numerize.numerize import numerize
########################### Initial settings for the dashboard ##################################################################
# Configure Seaborn with advanced color palettes
sns.set_theme(style="whitegrid", palette="colorblind")
########################### Initial settings for the dashboard ##################################################################
st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")

# Define side bar
st.sidebar.title("Page Selector")
page = st.sidebar.selectbox('Select a page of the analysis',
  ["Intro", "Weather component and bike usage", "Most popular stations", "Interactive map with aggregated bike trips", "Recommendations"])
########################## Import data ###########################################################################################
df = pd.read_csv('red_data_to_plot_7.csv', index_col=None)
df_w= pd.read_csv('NY_weather.csv', index_col = 0)


### Intro page

if page == 'Intro':
    st.markdown("#### This dashboard aims to provide insights about the best way to expand City Bike services.")
    st.markdown("Right now, Citi Bike customers complain about bikes not being available at certain times in popular locations. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Page Selector' will take you to the different pages of the analysis our team looked at.")

    myImage = Image.open("cropped-picture.jpg") #source: https://www.freepik.com/
    st.image(myImage)

elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df_w['date'], y = df_w['bike_rides_daily'], name = 'Daily bike rides', 
               marker={'color': '#3B719F'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df_w['date'], y = df_w['avgTemp'], name = 'Daily temperature', 
               marker={'color': '#CB4C4E'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title_text="Daily Bike Rides and Temperature",
    xaxis_title="Date",
    height = 400
    )

# Update y-axis titles (primary and secondary)
    fig_2.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)  # Primary y-axis label
    fig_2.update_yaxes(title_text="Temperature (°C)", secondary_y=True)  # Secondary y-axis label

    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("There is a strong correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily during the year 2022. As temperatures plunge, so does bike usage, mainly from late autumn to early summer. This insight indicates that the shortage problem may be prevalent mostly in the warmer months, approximately from May to Septermber.")

### Most popular stations page
# Create the season variable

elif page == 'Most popular stations':
    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart

    df1['value'] = 1 
    df1_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df1_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'spectral'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St emerged as the top trip generators. These account for a large share of total rides, where usage declines steeply beyond the top 5, indicating a skewed distribution where a few stations bear most of the load. These stations are prone to bike shortages during peak hours and seasons. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "NY_dash.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.markdown("Trip density maps show that Central and lower Manhattan are the most popular areas for bike trips. This might be explained by popular tourist destinations and numerous commercial areas.")
    st.markdown("There are a lot of trips across major bridges, especially between Manhattan, Brooklyn, and Jersey City. This shows that commuting between these areas should be prioritized when considering Cike Bike distribution across the city, expecially during peak hours.")
    st.components.v1.html(html_data,height=700)
    
else:

    st.header("Conclusions and recommendations")
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St")
    st.markdown("- Ensure that bikes are fully stocked in all these stations between May and September in order to meet the higher demand, but provide a lower supply in late autumn, winter, and early spring to reduce logistics costs.")
    st.markdown("- Unpopular areas, such as Northern Manhattan and eastern Queens, should be promoted by offering discouts or similar strategies, to address underutilization.")
    bikes = Image.open("man-woman-riding-their-bikes.jpg")  #source: https://www.freepik.com/
    st.image(bikes)
    
