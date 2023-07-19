import folium

# Latitude and Longitude pairs
coordinates = [
    (41.31397449192338, -105.5776558322157),
    (42.3601, -71.0589),
    (37.7749, -122.4194),
    # Add more pairs here...
]

# Create a map centered on the first pair
map_center = coordinates[0]
m = folium.Map(location=map_center, zoom_start=10)

# Add markers for each coordinate pair
for coord in coordinates:
    folium.Marker(location=coord).add_to(m)

# Save the map as an HTML file
m.save("map.html")
