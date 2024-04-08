# main.py
from cloud import CloudinaryModule
from catalogo import CatalogModule
from json_save import JsonModule
from fire import FirebaseModule
import json

# Create an instance of the CloudinaryModule class
cloudinary_module = CloudinaryModule('cloudinary_config.json')

# Get the resources using the get_resources method
resources = cloudinary_module.get_resources()

# Create a dictionary where the key is the image reference and the value is the image URL
image_dict = {resource['public_id'].replace('catalogo/', ''): resource['url'] for resource in resources}

# Create an instance of the CatalogModule class
catalog_module = CatalogModule(r'Catálogo.xlsx')

# Get the processed data
data_final = catalog_module.data_final

# Get the processed DataFrame
df_filtrado = catalog_module.df

# Convert the 'ref' column to string
df_filtrado['ref'] = df_filtrado['ref'].astype(str)

# Add a new column to the DataFrame with the image URLs
df_filtrado['imagem'] = df_filtrado['ref'].map(image_dict)

# If there is no image for a certain item, the value in the 'imagem' column will be NaN.
# You can replace these NaN values with an empty string like this:
df_filtrado['imagem'] = df_filtrado['imagem'].fillna('')

# Create an instance of the JsonModule class
json_module = JsonModule()

# Save the DataFrame as a JSON file
json_data = df_filtrado.to_dict(orient="records")
json_module.save_json(json_data, 'Catalogo.json')

# Create an instance of the FirebaseModule class
firebase_module = FirebaseModule(
    "fire_config.json",
    "https://catalogo-93491-default-rtdb.firebaseio.com/"
)

# Transform the data so that the 'ref' key is used as the key for each object
json_data = {item['ref']: item for item in json_data}

# Delete the old data
firebase_module.delete_data()

# Save the new data
firebase_module.save_data_to_firebase(json_data)
