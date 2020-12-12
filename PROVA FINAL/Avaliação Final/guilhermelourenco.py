#!/usr/bin/env python
# coding: utf-8

# ### GUILHERME LOURENÇO
# 
# ## <span style="color:blue"> MBA em Ciência de Dados</span>
# ## <span style="color:blue">Técnicas Avançadas de Captura e Tratamento de Dados</span>
# 
# ### <span style="color:blue">Questão Avaliação Final - instruções</span>
# **Luis Gustavo Nonato** e **Moacir Antonelli Ponti**<br>
# 
# **Cemeai - ICMC/USP São Carlos**

# <font color='blue'> 
# *INSTRUÇÕES*:<br>
# 1) Você deve exportar o notebook que utilizou para resolver as questões da prova em formato .py e fazer upload no Moodle. Atenção: você não deve fazer upload de um arquivo notebook (.ipynb), mas sim um arquivo texto .py contendo os códigos python que utilizou para resolver as questões. O arquivo .py pode ser gerado através da opção:<br>
# File --> Download as --> Python (.py)
# disponível no Jupyter Notebook.
# 
# ou
# File --> Download .py
# no Google Colab
# 
# Caso não esteja utilizando o Jupyter, copie e cole seu código em um arquivo ASCII (Texto) salvando com a extensão .py
# 
# 2) O arquivo deve ser nomeado com seu nome e sobrenome, sem espaços. Exemplo: moacirponti.py
# 
# 3) É OBRIGATÓRIO conter no cabeçalho (início) do arquivo um comentário / texto com o seu nome completo
# 
# ------------------
# </font>

# In[1]:


URL = "https://ckan.pbh.gov.br/dataset/c43b45d5-fe41-4099-b1a7-a0c76dfd45a6/resource/18372718-8c7a-424e-ac56-0cfbfc4badea/download/contratacaocorona-27-07-acertado.csv"


# ----
# O arquivo `contratacaocorona-27-07-acertado.csv` contém informações de compras emergenciais ligadas a COVID 19. 
# 
# 1. Leia o arquivo e considere apenas as colunas 'QUANTIDADE', 'VALOR_UNITM-ARIO' e 'VALOR_TOTAL'. Verifique quantos dados faltantes existem no DataFrame resultante.
# 2. Remova as linhas do data frame que contenham dados faltantes. Verifique quantas linhas foram removidas.
# 3. Prepare a coluna 'VALOR_TOTAL' para ser processada como numérica, e a seguir busque por outliers presentes nesta coluna. Para isso use o método do desvio padrão com $\sigma=3$. Verifique o número de outliers encontrados.
# 
# Com base nos itens acima, assinale a alternativa correta
# 
# a) Dados faltantes: 12, Linhas removidas: 12, Outliers encontrados: 6<br>
# b) Dados faltantes: 30, Linhas removidas: 30, Outliers encontrados: 2<br>
# c) Dados faltantes: 12, Linhas removidas: 12, Outliers encontrados: 4<br>
# d) Dados faltantes: 30, Linhas removidas: 24, Outliers encontrados: 6<br>
# <font color='red'>e) Dados faltantes: 30, Linhas removidas: 12, Outliers encontrados: 4</font>

# ### Etapa 1:
# Leia o arquivo e considere apenas as colunas 'QUANTIDADE', 'VALOR_UNITM-ARIO' e 'VALOR_TOTAL'. Verifique quantos dados faltantes existem no DataFrame resultante.

# In[2]:


import pandas as pd

corona = pd.read_csv(URL, sep=';', usecols=['QUANTIDADE', 'VALOR_UNITM-ARIO', 'VALOR_TOTAL'])
qtd_nulos = corona.isna().values.sum()
print(f'TAMANHO DA BASE: {len(corona)}\nDADOS FALTANTES: {qtd_nulos}')


# ### Etapa 2:
# Remova as linhas do data frame que contenham dados faltantes. Verifique quantas linhas foram removidas.

# In[3]:


corona_sem_nulo = corona.dropna()
print(f'TAMANHO DA BASE SEM NULO: {len(corona_sem_nulo)}\nDADOS FALTANTES: {corona_sem_nulo.isna().values.sum()}\nDADOS REMOVIDOS: {len(corona) - len(corona_sem_nulo)}')


# ### Etapa 3:
# Prepare a coluna 'VALOR_TOTAL' para ser processada como numérica, e a seguir busque por outliers presentes nesta coluna. Para isso use o método do desvio padrão com σ = 3. Verifique o número de outliers encontrados.

# In[4]:


corona_valor_total = corona_sem_nulo.copy()
corona_valor_total['VALOR_TOTAL_AJUSTADO'] = corona_valor_total['VALOR_TOTAL'].str.replace('R', '')
corona_valor_total['VALOR_TOTAL_AJUSTADO'] = corona_valor_total['VALOR_TOTAL_AJUSTADO'].str.replace('$', '')
corona_valor_total['VALOR_TOTAL_AJUSTADO'] = corona_valor_total['VALOR_TOTAL_AJUSTADO'].str.replace('.', '')
corona_valor_total['VALOR_TOTAL_AJUSTADO'] = corona_valor_total['VALOR_TOTAL_AJUSTADO'].str.replace(',', '.')

corona_valor_total['VALOR_TOTAL_AJUSTADO']=pd.to_numeric(corona_valor_total['VALOR_TOTAL_AJUSTADO'])
corona_valor_total.head()


# In[5]:


def detecta_outliers(df, variable):
    q1 = df[variable].quantile(0.25)
    q3 = df[variable].quantile(0.75)
    iqr = q3 - q1

    desvp = df[variable].std()
    media = df[variable].mean()

    matches = df[(df[variable] < media-(desvp*3)) | (df[variable] > media+(desvp*3))]

    return len(matches)


# In[6]:


qtd_outliers = detecta_outliers(corona_valor_total, 'VALOR_TOTAL_AJUSTADO')
print(f'TAMANHO DA BASE ORIGINAL: {len(corona)}\nDADOS FALTANTES: {qtd_nulos}\nDADOS REMOVIDOS: {len(corona) - len(corona_sem_nulo)}\nTOTAL DE OUTLIERS {qtd_outliers}')


# In[ ]:




