import requests
import os
import zipfile
import shutil

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
for file in os.listdir('shapefile'):
    if file.endswith('.db'):
        db_file = os.path.join('shapefile', file)
        break

if db_file:
    # Define the destination path for the DB file
    destination_path = 'scheduled/modis.ba.poly.db' 

    # Copy the DB file to the destination path
    shutil.copy(db_file, destination_path)

    print("DB file saved as:", destination_path)
else:
    print("DB file not found.")

# Clean up the zip file and the extracted folder
os.remove('shapefile.zip')
shutil.rmtree('shapefile')
