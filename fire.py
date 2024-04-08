import firebase_admin
from firebase_admin import credentials, db

class FirebaseModule:
    def __init__(self, config, databaseURL):
        self.config = config
        self.databaseURL = databaseURL
        self.initialize_app()

    def initialize_app(self):
        # Inicializa o aplicativo Firebase com as credenciais e URL do banco de dados
        cred = credentials.Certificate(self.config)
        firebase_admin.initialize_app(cred, {
            'databaseURL': self.databaseURL
        })

    def save_data_to_firebase(self, json_data):
        # Referência ao nó 'produtos' no Realtime Database
        ref = db.reference('produtos')

        try:
            # Salva os dados do JSON na base de dados Firebase
            ref.set(json_data)
            print("Dados salvos com sucesso no Firebase!")
        except Exception as e:
            print(f"Erro ao salvar dados no Firebase: {e}")

    def delete_data(self):
        # Referência ao nó 'produtos' no Realtime Database
        ref = db.reference('produtos')

        try:
            # Deleta os dados do nó 'produtos'
            ref.delete()
            print("Dados deletados com sucesso do Firebase!")
        except Exception as e:
            print(f"Erro ao deletar dados do Firebase: {e}")
