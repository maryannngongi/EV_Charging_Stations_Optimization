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
from sklearn.cluster import KMeans
import sklearn

# Page configuration
st.set_page_config(
    page_title="Kenya EV Charging Station Optimizer",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Kenya EV Charging Station Location Optimizer")
st.markdown("""
This application uses population data and machine learning to recommend optimal locations 
for electric vehicle charging stations across Kenyan counties.
""")

# Load data
@st.cache_data
def load_data():
    county_df = pd.read_csv("./Data/processed/county_data_clean.csv")
    kenya_stations = pd.read_csv("./Data/processed/kenya_stations_clean.csv")
    return county_df, kenya_stations

county_df, kenya_stations = load_data()

# Load models
@st.cache_resource
def load_models():
    additional_station_model = joblib.load("./ml_models/additional_station_model.joblib")
    county_kmeans_models = joblib.load("./ml_models/county_models.joblib")
    return additional_station_model, county_kmeans_models

additional_station_model, county_kmeans_models = load_models()

# Sidebar
st.sidebar.title("User Input")
selected_county = st.sidebar.selectbox("Select County", county_df["county"].unique())
population_input = st.sidebar.number_input("Enter Population (Optional)", min_value=0, value=0)
existing_stations_input = st.sidebar.number_input("Enter Existing Stations (Optional)", min_value=0, value=0)
predict_button = st.sidebar.button("Predict Stations and Locations")


def allocate_new_stations(county, kenya_stations, k):
    county_name = county["county"]
    county_stations = kenya_stations[
        kenya_stations["county"] == county_name
    ]
    
    existing_coords = county_stations[["latitude","longitude"]].values
    # If no additional stations needed
    if k == 0:
        return None, [], None
    np.random.seed(42)
    county_lat = county["county_lat"]
    county_lon = county["county_lon"]
    synthetic_points = []
    for _ in range(max(k*5, 20)):
        synthetic_points.append([
            county_lat + np.random.uniform(-0.063, 0.063),
            county_lon + np.random.uniform(-0.063, 0.063)
        ])
    synthetic_points = np.array(synthetic_points)
    # Combine existing + synthetic
    if len(existing_coords) > 0:
        training_points = np.vstack([existing_coords, synthetic_points])
    else:
        training_points = synthetic_points
    # Run ONE KMeans model
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(training_points)
    return kmeans, kmeans.cluster_centers_, training_points

st.write("Sklearn version:", sklearn.__version__)

# Prediction logic
if predict_button:

    county_data = county_df[county_df["county"] == selected_county].iloc[0]

    population = population_input if population_input > 0 else county_data["population"]
    num_stations = existing_stations_input if existing_stations_input > 0 else county_data["num_stations"]
    shape_area = county_data["shape area"]

    population_density = population / shape_area
    station_spatial_density = num_stations / shape_area

    X_input = pd.DataFrame([{
        "population": population,
        "population_density": population_density,
        "num_stations": num_stations,
        "station_spatial_density": station_spatial_density,
        "shape area": shape_area
    }])

    predicted_additional = additional_station_model.predict(X_input)[0]
    predicted_additional = int(np.round(predicted_additional))

    st.success(f"Predicted Additional Stations for {selected_county}: {predicted_additional}")

    # Run dynamic KMeans allocation
    kmeans_model, centers, training_points = allocate_new_stations(
        county_data,
        kenya_stations,
        predicted_additional
    )

    if predicted_additional == 0:
        st.info("No additional stations needed for this county.")
    else:
        new_stations_df = pd.DataFrame(
            centers,
            columns=["latitude", "longitude"]
        )

        st.subheader("Predicted New Station Locations")
        st.dataframe(new_stations_df)

        st.subheader("Station Map")

        m = folium.Map(
            location=[county_data["county_lat"], county_data["county_lon"]],
            zoom_start=9
        )

        county_existing = kenya_stations[
            kenya_stations["county"] == selected_county
        ]

        for _, row in county_existing.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                color="blue",
                fill=True,
                fill_color="blue",
                popup="Existing Station"
            ).add_to(m)

        for _, row in new_stations_df.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=6,
                color="red",
                fill=True,
                fill_color="red",
                popup="Predicted Station"
            ).add_to(m)

        folium_static(m)