import json
import cloudinary
import cloudinary.api

class CloudinaryModule:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = json.load(file)
        self.initialize_config()

    def initialize_config(self):
        # Inicializa a configuração do Cloudinary com as configurações fornecidas
        cloudinary.config(
            cloud_name=self.config['cloud_name'],
            api_key=self.config['api_key'],
            api_secret=self.config['api_secret'],
            secure=True,
        )

    def get_resources(self):
        resources = []
        next_cursor = None
        while True:
            response = cloudinary.api.resources(max_results=500, next_cursor=next_cursor)
            resources.extend(response['resources'])
            next_cursor = response.get('next_cursor')
            if not next_cursor:
                break
        return resources