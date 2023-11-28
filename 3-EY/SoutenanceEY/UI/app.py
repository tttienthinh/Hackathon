import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

df = pd.read_csv("5-Regression.csv")
# df = pd.read_csv("Crop_Yield_Data_challenge_2.csv")

# col1, col2 = st.columns(2)
# col1.date_input()
st.set_page_config(
    page_title="EY 🌾",
    page_icon="chart_with_upwards_trend"
)
st.title("EY Rice predict")
st.date_input("Entrez les dates à analyser (non fonctionnel)", value=(datetime(2022, 4, 10), datetime(2023, 12, 1)))

fig = px.scatter_mapbox(
    df, 
    lat="Latitude", 
    lon="Longitude", 
    zoom=4,
    hover_name="District",
    hover_data=["Predicted Rice Yield (kg/ha)", "Date of Harvest", "Field size (ha)", "Season(SA = Summer Autumn, WS = Winter Spring)"]
)

fig.update_layout(mapbox_style="stamen-terrain")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)