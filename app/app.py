import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys
from pathlib import Path
# Page configuration
st.set_page_config(
    page_title="Kenya EV Charging Station Optimizer",
    page_icon="⚡",
    layout="wide"
)
# Title and introduction
st.title("⚡ Kenya EV Charging Station Location Optimizer")
st.markdown("""
This application uses population data and machine learning to recommend optimal locations 
for electric vehicle charging stations across Kenyan counties.
""")
# Load data
@st.cache
def load_data():
    county_df = pd.read_csv("./utilities/county_data_clean.csv")
    kenya_stations = pd.read_csv("./utilities/kenya_stations_clean.csv")
    new_stations = pd.read_csv("./utilities/new_stations.csv")
    return county_df, kenya_stations, new_stations

county_df, kenya_stations, new_stations = load_data()
# Load model
@st.cache
def load_models():
    additional_station_model = joblib.load("../ml_models/additional_station_model.joblib")
    county_kmeans_models = joblib.load("../ml_models/county_models.joblib")
    return additional_station_model, county_kmeans_models

additional_station_model, county_kmeans_models = load_models()
# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Infrastructure Gap Analysis", "Station Placement", "Future Projections", "About"]
)
st.sidebar.header("User Input")

selected_county = st.sidebar.selectbox(
    "Select County",
    county_df["county"].unique()
)

population_input = st.sidebar.number_input(
    "Enter Population (Optional)",
    min_value=0,
    value=0
)

existing_stations_input = st.sidebar.number_input(
    "Enter Existing Stations (Optional)",
    min_value=0,
    value=0
)

predict_button = st.sidebar.button("Predict Stations")

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Current EV Charging Infrastructure Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_stations = county_df['num_stations'].sum()
        st.metric("Total Charging Stations", int(total_stations))

    with col2:
        counties_with_stations = len(county_df[county_df['num_stations'] > 0])
        st.metric("Counties with Stations", counties_with_stations)

    with col3:
        total_population = county_df['population'].sum()
        st.metric("Total Population Covered", f"{total_population:,.0f}")

    with col4:
        required = county_df['required_stations'].sum()
        st.metric("Total Stations Needed", int(required))
elif page == "Infrastructure Gap Analysis":

    st.header("📉 Infrastructure Gap Analysis")

    # Sort by additional stations
    gap_df = county_df.sort_values("additional_stations", ascending=False)

    fig = px.bar(
        gap_df,
        x="additional_stations",
        y="county",
        orientation="h",
        title="Additional Stations Required per County",
        color="additional_stations"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 5 Counties with Highest Infrastructure Gap")

    st.dataframe(gap_df[["county", "population", "num_stations", 
                         "required_stations", "additional_stations"]].head())
elif page == "Station Placement":

    st.header("Optimized EV Charging Station Locations")

    kenya_map = folium.Map(location=[0.5, 37], zoom_start=6)

    # Existing stations
    for _, row in kenya_stations.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            popup=row["station name"],
            color="green",
            fill=True
        ).add_to(kenya_map)

    # Predicted stations
    for _, row in new_stations.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            popup=row["county"],
            color="blue",
            fill=True
        ).add_to(kenya_map)

    st.markdown("Green = Existing Stations  |   Blue = Recommended Stations")

    folium_static(kenya_map)       