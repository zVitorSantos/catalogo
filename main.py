import pandas as pd
import json
from collections import Counter

# Ler o arquivo .xlsx
df = pd.read_excel(r'Catálogo.xlsx')

# Extrair as colunas desejadas e renomear
df = df[["REF.:", "DESCRIÇÃO DO PRODUTO", "MEDIDAS MM HxL", "MATERIAL", "PESO", "M.", "P.", "D."]]
df.columns = ["ref", "descricao", "medidas", "material", "peso", "matriz", "piloto", "desenho"]

# Converter as medidas para altura e largura
df["altura"] = df["medidas"].str.split("x").str[0]
df["largura"] = df["medidas"].str.split("x").str[1]

# Converter os valores da coluna 'ref' para inteiros
df['ref'] = pd.to_numeric(df['ref'], errors='coerce')  # 'coerce' para lidar com strings não numéricas

# Filtrar o DataFrame para incluir apenas produtos com referência menor ou igual a 5250
df_filtrado = df[df['ref'] <= 5250].copy()  # Fazer uma cópia para evitar alterações no DataFrame original

# Listas de palavras para cada prioridade
prioridade_1 = ['bioluz', 'brilha', 'brilha natal', 'natal', 'sousplat', 'tdecorare']
prioridade_2 = ['bridão', 'âmago', 'passador', 'fivela', 'ornavi', 'pingente', 'salomé', 'animais', 'tira']
prioridade_3 = ['laço', 'flor', 'coração', 'botão', 'mandala', 'pedra']
complementos = ['resina', 'strass']
modelos = ['i', 't', 'y', 'v']

def buscar_palavras(descricao):
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

# Aplicar a função 'buscar_palavras' e armazenar o resultado nas colunas correspondentes
categorias = df_filtrado['descricao'].apply(buscar_palavras)
df_filtrado[['categoria_1', 'categoria_2', 'categoria_3', 'complementos']] = categorias

# Substituir valores NaN por uma string vazia
df_filtrado = df_filtrado.fillna('')

# Remover espaços no início e no fim das strings
df_filtrado = df_filtrado.apply(lambda x: x.map(lambda y: y.strip() if isinstance(y, str) else y))

# Considerar qualquer valor não vazio como True
df_filtrado[['matriz', 'piloto', 'desenho']] = df_filtrado[['matriz', 'piloto', 'desenho']].apply(lambda x: x.map(lambda y: False if y == '' else True))

# Adicionar a coluna 'valor' ao DataFrame
df_filtrado['valor'] = ""

# Converter os valores da coluna 'ref' para inteiros, ignorando os valores NaN
df_filtrado['ref'] = df_filtrado['ref'].apply(lambda x: int(x) if pd.notnull(x) else x)

# Converter o DataFrame filtrado para uma lista de dicionários mantendo a ordem das colunas
data = df_filtrado[["ref", "descricao", "categoria_1", "categoria_2", "categoria_3", "complementos", "altura", "largura", "material", "peso", "valor", "matriz", "piloto", "desenho"]].to_dict(orient="records")

# Criar o dicionário final para salvar como JSON
data_final = {"produtos": data}

# Salvar o dicionário como um arquivo JSON
with open('Catalogo.json', 'w', encoding='utf-8') as file:
    json.dump(data_final, file, ensure_ascii=False, indent=4)