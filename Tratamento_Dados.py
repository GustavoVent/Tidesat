import pandas as pd
import requests
from io import StringIO
from datetime import datetime,timedelta


def tratamento_dados(data_lines):
    # Create a DataFrame using the data_lines, excluding the first line
    df_remov = pd.read_csv(StringIO('\n'.join(data_lines[1:])), header=None)

    # Replace multiple consecutive spaces with a single space in the entire DataFrame
    df_dados_I = df_remov.replace('\s+', ' ', regex=True)
    df_dados = df_dados_I.apply(lambda x: x.str.replace(r'(?<=.)\s+', ';', regex=True))

    # Remove the last character from each element in the DataFrame
    df_dados_removed_last = df_dados.apply(lambda x: x.str.slice(0, -1))

    # Load only the first 8 rows
    #df_dados_first_8 = df_dados_removed_last.head(8)

    return df_dados_removed_last


url = "http://app.tidesatglobal.com/sph4/sph4_2023_spline_out.txt"
# Baixar os dados da URL
response = requests.get(url)
# Dividir o conteúdo em linhas
lines = response.text.split('\n')
# Remover as três primeiras linhas
data_lines = lines[3:]
# Inicializar variável para cabeçalho
cabecalho = None
# Ler a terceira linha como cabeçalho
dados = []
# Carregando os dados
dados = tratamento_dados(data_lines)

# Separando os dados em colunas usando ponto e vírgula como delimitador
dados_separados = dados[0].str.split(';', expand=True)

# Renomeando as colunas se necessário
dados_separados.columns = ['MJD', 'RH(m)', 'YY', 'MM1', 'DD', 'HH', 'MM', 'SS']

# Criação da coluna 'Data' e 'Hora'
dados_separados['Data'] = dados_separados[['YY', 'MM1', 'DD']].apply(lambda x: '-'.join(x.astype(str)), axis=1)
dados_separados['Hora'] = dados_separados[['HH', 'MM', 'SS']].apply(lambda x: ':'.join(x.astype(str)), axis=1)

# Criação da coluna 'Data_Hora' combinando 'Data' e 'Hora'
dados_separados['Data_Hora'] = dados_separados['Data'] + ' ' + dados_separados['Hora']

# Converta a coluna 'Data_Hora' para o formato de datetime
dados_separados['Data_Hora'] = pd.to_datetime(dados_separados['Data_Hora'], format="%Y-%m-%d %H:%M:%S")

# Ajuste o fuso horário subtraindo 3 horas
dados_separados['Dt_Final'] = dados_separados['Data_Hora'] + pd.DateOffset(hours=-3)

# Remova as três últimas colunas originais
dados_separados = dados_separados.drop(['YY', 'MM1', 'DD', 'HH', 'MM', 'SS', 'Data', 'Hora', 'Data_Hora'], axis=1)



# Agora você pode renomear as colunas
dados_separados.columns = ['MJD', 'RH(m)', 'Dt_Final']

# Imprima os dados se desejar
print(dados_separados)


# Aplicando a função Trans_data se necessário
#rf_data = Trans_data(dados_separados)



