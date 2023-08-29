import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd


# Load the environment file
load_dotenv(".env")

# Read the access token
access_token = os.getenv("MAPBOX_ACCESS_TOKEN")

def get_coordinates(municipality, state):
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

    query = f"{municipality}, {state}, Brazil.json?access_token={access_token}"

    url = base_url + query

    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['features']:
            longitude, latitude = data['features'][0]['geometry']['coordinates']
            return latitude, longitude
        else:
            return None
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

"""
locations = [
        {"municipality": "São Paulo", "state": "São Paulo"},
        {"municipality": "Rio de Janeiro", "state": "Rio de Janeiro"},
        {"municipality": "Salvador", "state": "Bahia"}
    ]


for location in locations:
    municipality = location["municipality"]
    state = location["state"]
    coordinates = get_coordinates(municipality, state)
    if coordinates:
        latitude, longitude = coordinates
        print(f"The coordinates for {municipality}, {state} are (Latitude: {latitude}, Longitude: {longitude})")
    else:
        print(f"Could not find coordinates for {municipality}, {state}")
"""

folder_path = "/raw_data/"
file_name = "municipality_lookup_4.csv"
file_path = os.path.join(os.getcwd()+folder_path, file_name)

df = pd.read_csv(file_path)

# Initialize empty lists to store latitude and longitude
latitudes = []
longitudes = []

# Loop through the DataFrame and get coordinates
for index, row in df.iterrows():
    municipality = row['Município']
    state = row['Estado']

    # Use the get_coordinates function to get the latitude and longitude
    coordinates = get_coordinates(municipality, state)

    if coordinates:
        latitude, longitude = coordinates
        latitudes.append(latitude)
        longitudes.append(longitude)
        print(f"The coordinates for {municipality}, {state} are (Latitude: {latitude}, Longitude: {longitude})")

    else:
        latitudes.append(None)
        longitudes.append(None)
        print(f"Could not find coordinates for {municipality}, {state}")


# Add latitude and longitude as new columns in the DataFrame
df['Latitude'] = latitudes
df['Longitude'] = longitudes

folder_path = "/transformed_data/"
file_name = "municipality_lookup_4.csv"
file_path = os.path.join(os.getcwd()+folder_path, file_name)
df.to_csv(file_path, index=False)
print("Done!!")
