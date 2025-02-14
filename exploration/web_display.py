import folium
import geopandas as gpd
import numpy as np
import pandas as pd

# Load the GeoDataFrame
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Function to style each country feature (optional, for better visibility)
def style_function(feature):
    return {
        'fillColor': '#b0de5c',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6,
    }

# Add GeoJSON layer with a popup for each country
folium.GeoJson(
    world,
    name="Countries",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['name', 'pop_est', 'gdp_md_est'],
        aliases=['Country:', 'Population:', 'GDP (Million USD):'],
        localize=True
    ),
    popup=folium.GeoJsonPopup(
        fields=['name', 'pop_est', 'gdp_md_est'],
        aliases=['Country:', 'Population:', 'GDP (Million USD):'],
        localize=True,
        labels=True,
        style="background-color: white; color: black; font-weight: bold; width: auto;"
    )
).add_to(m)

# Generate random data for research institutes
num_institutes = 50  # Number of random institutes
np.random.seed(0)  # Seed for reproducibility
lats = np.random.uniform(-60, 80, num_institutes)  # Random latitudes
lons = np.random.uniform(-180, 180, num_institutes)  # Random longitudes
importance = np.random.randint(1, 100, num_institutes)  # Random importance scale 1-100

# Add a bubble (circle marker) for each research institute
for lat, lon, imp in zip(lats, lons, importance):
    folium.CircleMarker(
        location=[lat, lon],
        radius=imp / 10,  # Adjust radius proportional to importance
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        tooltip=f"Research Institute - Importance: {imp}"
    ).add_to(m)

# Save the map as an HTML file
m.save('world_map_with_popups_and_bubbles.html')
