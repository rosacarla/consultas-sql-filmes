# -*- coding: utf-8 -*-
"""Cópia_de_consultas_SQL_top1000_filmes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/rosacarla/consultas-sql-filmes/blob/main/C%C3%B3pia_de_consultas_SQL_top1000_filmes.ipynb

# **TRABALHO INDIVIDUAL: consultas SQL em base de dados sobre filmes**

> ###### ATENÇÃO!
> ###### - Faça o upload do arquivo CSV no Colab;
> ###### - Ao lado, clique nos ícones de pasta e folha (com seta para cima) para começar a transferência.
> ###### - Clique no botão play ▶ em cada célula para executar uma após a outra.

> ### PRÉ-PROCESSAMENTO DA BASE DE DADOS
"""

# Preparação do ambiente
# Use a biblioteca Pandas para carregar o CSV e o SQLite para consultas SQL.
import pandas as pd
import sqlite3

# Carrega a planilha em formato CSV e salva a base de dados com o nome "filmes"
filmes = pd.read_csv('/content/Highest Holywood Grossing Movies.csv')

# Exibe primeiras linhas da base de dados
filmes.head(5)

# Mostra informações resumidas da base de dados inicial
filmes.info()

# Mostra todos os nomes das colunas da base de dados
filmes.columns

# Renomeia as colunas com nomes em PT-BR
filmes = filmes.rename(columns={
    'Title': 'Titulo',
    'Movie Info': 'Sinopse',
    'Year': 'Ano',
    'Distributor': 'Distribuidora',
    'Budget (in $)': 'Orcamento (US$)',
    'Domestic Opening (in $)': 'Abertura Domestica (US$)',
    'Domestic Sales (in $)': 'Vendas Domesticas (US$)',
    'International Sales (in $)': 'Vendas Internacionais (US$)',
    'World Wide Sales (in $)': 'Vendas Globais (US$)',
    'Release Date': 'Lancamento',
    'Genre': 'Genero',
    'Running Time': 'Duracao',
    'License': 'Licenca'
})

# Remove coluna 'Unnamed: 0' (elimina repetição da ordem numérica das linhas)
filmes = filmes.drop(columns=['Unnamed: 0'])

# Converte coluna 'Lancamento' para o formato datetime64 (data numérica)
filmes['Lancamento'] = pd.to_datetime(filmes['Lancamento'], format='%d-%b-%y')

# Formata a coluna de data para 'dia-mes-ano'
filmes['Lancamento'] = filmes['Lancamento'].dt.strftime('%d-%m-%Y')

# Salva o novo dataset
filmes.to_csv('filmes_modificado.csv', index=False)

print("Dataset modificado, datas convertidas, e foi salvo com sucesso!")

# Exibe primeiras linhas da base de dados modificada
filmes.head(5)

# Conectar ao banco de dados SQLite
connect = sqlite3.connect(':memory:')
filmes.to_sql('filmes', connect, index=False, if_exists='replace')

"""> ### CONSULTAS SQL NA BASE DE DADOS MODIFICADA

###### 1. Obtenha apenas os títulos dos filmes e seus orçamentos.
"""

# Selecionar colunas específicas
query = "SELECT Titulo, `Orcamento (US$)` FROM filmes;"
results = pd.read_sql_query(query, connect)
results

"""###### 2. Liste todos os filmes lançados após o ano 2000, mostrando o título e o ano de lançamento."""

# Filtrar resultados
query = "SELECT Titulo, Ano FROM filmes WHERE Ano > 2000;"
results = pd.read_sql_query(query, connect)
results

"""###### 3. Liste os títulos dos filmes ordenados pelas vendas globais em ordem crescente, mostrando os valores."""

# Ordenar resultados
query = "SELECT Titulo, `Vendas Globais (US$)` FROM filmes ORDER BY `Vendas Globais (US$)`;"
results = pd.read_sql_query(query, connect)
results

"""###### 4. Conte quantos filmes da distribuidora "Walt Disney Studios Motion Pictures" existem na base de dados."""

# Contar registros
query = "SELECT COUNT(*) FROM filmes WHERE Distribuidora = 'Walt Disney Studios Motion Pictures';"
results = pd.read_sql_query(query, connect)
print("A distribuidora Walt Disney Studios Motion Pictures possui", results.iloc[0, 0], "filmes.")

"""###### 5. Calcule a média de vendas globais dos filmes lançados entre 1990 e 2000."""

# Usar funções de agregação
query = "SELECT AVG(`Vendas Globais (US$)`) FROM filmes WHERE Ano BETWEEN 1990 AND 2000;"
results = pd.read_sql_query(query, connect)
media_vendas = format(results.iloc[0, 0], ',.2f')
print(f"A média de vendas dos filmes entre 1990 e 2000 é de US$ {media_vendas}")

"""######  6. Calcule o total de vendas globais de filmes por distribuidora."""

# Agrupar resultados
query = "SELECT Distribuidora, SUM(`Vendas Globais (US$)`) AS Total_Vendas FROM filmes GROUP BY Distribuidora;"
results = pd.read_sql_query(query, connect)
results

"""###### 7. Liste as distribuidoras que têm mais de 50 filmes."""

# Filtrar Dados Agrupados com HAVING
query = "SELECT Distribuidora, COUNT(*) AS Total_Filmes FROM filmes GROUP BY Distribuidora HAVING Total_Filmes > 50;"
results = pd.read_sql_query(query, connect)
results

"""###### 8. Selecionar os filmes com maior venda doméstica e maior venda global, mostrando os valores."""

# Selecionar o filme com maior venda doméstica
query = "SELECT Titulo, `Vendas Domesticas (US$)` FROM filmes WHERE `Vendas Domesticas (US$)` = (SELECT MAX(`Vendas Domesticas (US$)`) FROM filmes);"
results = pd.read_sql_query(query, connect)

# Formatar o valor das vendas com separadores de milhares
vendas_formatadas = format(results.iloc[0, 1], ',.2f')
print("O filme com maior venda doméstica é:", results.iloc[0, 0], "com US$", vendas_formatadas)

# Selecionar o filme com maior venda global
query = "SELECT Titulo, `Vendas Globais (US$)` FROM filmes WHERE `Vendas Globais (US$)` = (SELECT MAX(`Vendas Globais (US$)`) FROM filmes);"
results = pd.read_sql_query(query, connect)

# Formatar o valor das vendas com separadores de milhares
vendas_formatadas = format(results.iloc[0, 1], ',.2f')
print("O filme com maior venda global é:", results.iloc[0, 0], "com US$", vendas_formatadas)

"""###### Parabéns por chegar ao final deste notebook. Aproveite para salvar uma cópia no seu Google Drive (no menu superior, clicando em Arquivo/Salvar uma cópia no Drive). Bons estudos! 🤩"""