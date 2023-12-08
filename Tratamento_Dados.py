#caminho_arquivo = 'C:/Users/gusta/OneDrive/Área de Trabalho/Randon/Spline_nivel_agua.txt'

import pandas as pd

# Ler o conteúdo do arquivo
caminho_arquivo = r'C:\Users\gfigu\OneDrive\Área de Trabalho\Projeto\Tidesat\tide01.txt'

# Inicializar variável para cabeçalho
cabecalho = None

# Ler a terceira linha como cabeçalho
with open(caminho_arquivo, 'r') as arquivo:
    for i, linha in enumerate(arquivo):
        if i == 3:  # Terceira linha (índice 2)
            cabecalho = linha.strip().split(',')[0:]  # Ignorar as duas primeiras casas
            break

# Ler os dados do arquivo usando o pandas
dados = pd.read_csv(caminho_arquivo, skiprows=4, delim_whitespace=True, header=None)

# Definir o cabeçalho
dados.columns = cabecalho

# Imprimir os dados como uma tabela
print(dados)


