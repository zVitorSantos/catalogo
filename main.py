import pandas as pd
import json
import re

# Ler o arquivo .xlsx
df = pd.read_excel(r'C:\Users\Vitor\Desktop\Programas\Catálogo JSON\Catálogo.xlsx')

# Extrair as colunas desejadas
df = df[["REF.:", "DESCRIÇÃO DO PRODUTO", "MEDIDAS MM HxL", "MATERIAL", "PESO", "M.", "P.", "D."]]

# Renomear as colunas
df.columns = ["ref", "descricao", "medidas", "material", "peso", "matriz", "piloto", "desenho"]

# Converter as medidas para altura e largura
df["altura"] = df["medidas"].str.split("x").str[0]
df["largura"] = df["medidas"].str.split("x").str[1]

# Selecionar apenas as colunas desejadas
df = df[["ref", "descricao", "altura", "largura", "material", "peso", "matriz", "piloto", "desenho"]]

# Adicionar novas colunas
df.insert(df.columns.get_loc("peso") + 1, "custo", "")
df.insert(df.columns.get_loc("descricao") + 1, "categoria_1", "")
df.insert(df.columns.get_loc("categoria_1") + 1, "categoria_2", "")
df.insert(df.columns.get_loc("categoria_2") + 1, "categoria_3", "")

# Lista de categorias para buscar na descrição
categorias = ['bridão', 'âmago', 'passador', 'fivela', 'ornavi', 'pingente', 'laço', 'salomé', 'animais', 'coração']

# Função para buscar categorias na descrição
def buscar_categorias(descricao):
    if isinstance(descricao, str):  # Verificar se a descrição é uma string
        descricao = descricao.lower()  # Converter a descrição para minúsculas
        # Tratar 'Bioluz', 'brilha', 'brilha natal' e 'natal' de maneira especial
        if any(word in descricao for word in ['bioluz', 'brilha', 'brilha natal', 'natal']):
            return ['Bioluz' if 'bioluz' in descricao else 'Brilha Natal', '', '']
        
        # Para todas as outras categorias, preenchê-las na ordem em que aparecem na descrição
        categorias_encontradas = [categoria for categoria in categorias if categoria in descricao][:3]  # Limitar a 3 categorias
        
        # Extrair o formato após "Tira em "
        match = re.search(r'tira em (\w+)', descricao)
        if match and 'Tira' not in categorias_encontradas:  
            categorias_encontradas = categorias_encontradas[:2] 
            categorias_encontradas.append('Tira')
            categorias_encontradas.append(match.group(1))
        
        return categorias_encontradas + [''] * (3 - len(categorias_encontradas)) 
    else:
        return ['', '', '']

# Aplicar a função para buscar categorias
df[['categoria_1', 'categoria_2', 'categoria_3']] = pd.DataFrame(df['descricao'].apply(buscar_categorias).tolist(), index=df.index)

# Aplicar a função para buscar categorias
df[['categoria_1', 'categoria_2', 'categoria_3']] = pd.DataFrame(df['descricao'].apply(buscar_categorias).tolist(), index=df.index)
# Substituir valores NaN por uma string vazia
df = df.fillna('')

# Remover espaços no início e no fim das strings
df = df.apply(lambda x: x.map(lambda y: y.strip() if isinstance(y, str) else y))

# Considerar qualquer valor não vazio como True
df[['matriz', 'piloto', 'desenho']] = df[['matriz', 'piloto', 'desenho']].apply(lambda x: x.map(lambda y: False if y == '' else True))

# Converter o DataFrame para um dicionário
data = {"produtos": df.to_dict(orient="records")}

# Salvar o dicionário como um arquivo JSON
with open(r'C:\Users\Vitor\Desktop\Programas\Catálogo JSON\Catalogo.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)  # ensure_ascii=False para manter os caracteres especiais