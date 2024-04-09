# catalog_module.py
import pandas as pd

class CatalogModule:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.process_data()

    def process_data(self):
        # Extrair as colunas desejadas e renomear
        self.df = self.df[["REF.:", "DESCRIÇÃO", "MEDIDAS(A,L,C)", "MATERIAL", "PESO", "MATRIZ", "PILOTO", "DESENHO"]]
        self.df.columns = ["ref", "descricao", "medidas", "material", "peso", "matriz", "piloto", "desenho"]

        # Dividir as strings na coluna "medidas"
        medidas_divididas = self.df["medidas"].str.split("x", expand=True)
        
        # Atribuir os resultados às colunas "altura", "largura" e "comprimento"
        self.df["altura"] = pd.to_numeric(medidas_divididas[0].str.replace("mm", ""), errors='coerce')
        self.df["largura"] = pd.to_numeric(medidas_divididas[1].str.replace("mm", ""), errors='coerce')
        self.df["comprimento"] = pd.to_numeric(medidas_divididas[2].str.replace("mm", ""), errors='coerce')
        
        # Remover a coluna "medidas"
        self.df = self.df.drop(columns=["medidas"])

        # Converter os valores da coluna 'ref' para inteiros
        self.df['ref'] = pd.to_numeric(self.df['ref'], errors='coerce')  # 'coerce' para lidar com strings não numéricas

        # Filtrar o DataFrame para incluir apenas produtos com referência menor ou igual a 5250
        self.df = self.df[self.df['ref'] <= 5220].copy()  # Fazer uma cópia para evitar alterações no DataFrame original

        # Aplicar a função 'buscar_palavras' e armazenar o resultado nas colunas correspondentes
        categorias = self.df['descricao'].apply(self.buscar_palavras)
        self.df[['categoria_1', 'categoria_2', 'categoria_3', 'complementos']] = categorias
        
        # Substituir valores NaN por uma string vazia
        self.df = self.df.fillna('')

        # Remover espaços no início e no fim das strings
        self.df = self.df.apply(lambda x: x.map(lambda y: y.strip() if isinstance(y, str) else y))

        # Considerar qualquer valor não vazio como True
        self.df[['matriz', 'piloto', 'desenho']] = self.df[['matriz', 'piloto', 'desenho']].apply(lambda x: x.map(lambda y: False if y == '' else True))

        # Adicionar a coluna 'valor' ao DataFrame
        self.df['valor'] = ""
        
        # Adicionar a coluna 'imagem' ao DataFrame
        self.df['imagem'] = ''
        
        # Converter os valores da coluna 'ref' para inteiros, ignorando os valores NaN
        self.df['ref'] = self.df['ref'].apply(lambda x: int(x) if pd.notnull(x) else x)

        # Converter o DataFrame filtrado para uma lista de dicionários mantendo a ordem das colunas
        data = self.df[["ref", "imagem", "descricao", "categoria_1", "categoria_2", "categoria_3", "complementos", "altura", "largura", "comprimento", "material", "peso", "valor", "matriz", "piloto", "desenho"]].to_dict(orient="records")

        # Criar o dicionário final para salvar como JSON
        self.data_final = {"produtos": data}

    def buscar_palavras(self, descricao): 
        # Listas de palavras para cada prioridade
        prioridade_1 = ['bioluz', 'brilha', 'brilha natal', 'natal', 'sousplat', 'tdecorare']
        prioridade_2 = ['bridão', 'âmago', 'passador', 'fivela', 'ornavi', 'pingente', 'salomé', 'animais', 'tira']
        prioridade_3 = ['laço', 'flor', 'coração', 'botão', 'mandala', 'pedra']
        complementos = ['resina', 'strass']
        modelos = ['i', 't', 'y', 'v']
        
        categorias = pd.Series({
            "categoria_1": "",
            "categoria_2": "",
            "categoria_3": "",
            "complementos": ""
        })
        
        if isinstance(descricao, str):
            descricao = descricao.lower()
            
            # Verificar complementos na descrição
            complementos_encontrados = [complemento for complemento in complementos if complemento in descricao]
            if complementos_encontrados:
                categorias['complementos'] = ', '.join(complementos_encontrados).capitalize()
            
            # Verificar palavras de prioridade 1
            for palavra in prioridade_1:
                if palavra in descricao:
                    categorias['categoria_1'] = palavra.capitalize()
                    break  # Parar no primeiro match
            
            # Verificar palavras de prioridade 2
            for palavra in prioridade_2:
                if palavra in descricao:
                    if 'tira em' in descricao:
                        for modelo in modelos:
                            if f'tira em {modelo}' in descricao:
                                categorias['categoria_2'] = f'Tira em {modelo.capitalize()}'
                                return categorias
                    else:
                        categorias['categoria_2'] = palavra.capitalize()
                        break  # Parar no primeiro match
            
            # Verificar palavras de prioridade 3
            prioridade_3_encontradas = [palavra for palavra in prioridade_3 if palavra in descricao]
            if prioridade_3_encontradas:
                if len(prioridade_3_encontradas) == 1:
                    categorias['categoria_2'] = prioridade_3_encontradas[0].capitalize()
                else:
                    categorias['categoria_2'] = prioridade_3_encontradas[0].capitalize()
                    categorias['categoria_3'] = ', '.join(prioridade_3_encontradas[1:]).capitalize()
        
        return categorias