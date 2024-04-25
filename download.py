import requests
import os
import zipfile
import shutil
import fiona
import pandas as pd
import geopandas as gpd

# URL of the shapefile download endpoint
url = "https://maps.effis.emergency.copernicus.eu/effis?service=WFS&request=getfeature&typename=ms:modis.ba.poly&version=1.1.0&outputformat=SPATIALITEZIP"

# Download the shapefile zip file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the zip file to the current directory
    with open('shapefile.zip', 'wb') as f:
        f.write(response.content)

    print("Shapefile downloaded successfully.")
else:
    print("Failed to download the shapefile. Status code:", response.status_code)

# Unzip the shapefile
with zipfile.ZipFile('shapefile.zip', 'r') as zip_ref:
    zip_ref.extractall('shapefile')

# Find the DB file in the extracted folder
db_file = None
extracted_folder = 'shapefile'
for file in os.listdir(extracted_folder):
    if file.endswith('.db'):
        db_file = os.path.join(extracted_folder, file)
        break

# Create a GeoDataFrame from the DB file
if db_file:
    with fiona.open(db_file) as src:
        gdf = gpd.GeoDataFrame.from_features(src, crs=src.crs)
        print("GeoDataFrame created successfully.")
else:
    print("DB file not found.")

# Clean up the zip file and the extracted folder
os.remove('shapefile.zip')
shutil.rmtree('shapefile')


#Get the data only for Greece
el_gdf = gdf[gdf['country'] == 'FR']

# Define the destination path for saving the GeoDataFrame
destination_path = os.path.join('el_gdf.geojson')
el_gdf.to_file(destination_path, driver='GeoJSON')
