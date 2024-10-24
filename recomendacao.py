 # -*- coding: utf-8 -*-
"""continuação da aula.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ivQ9kuirj8k6LXGkKJj6YKmbj992jR1o
"""

#Importando as bibliotecas necessárias

#NumPy, uma biblioteca para manipulação de arrays e matrizes
import numpy as np
#KMeans, um algoritmo de agrupamento de dados
from sklearn.cluster import KMeans

import pandas as pd

caminho_arquivo = '/content/filmes_100_usuarios.csv'

df = pd.read_csv(caminho_arquivo)

print(df.head())



filmes_assistidos = df.drop(columns=["Unnamed: 0"]).values

# Treinar o modelo
# Numero de clusters(grupos)
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters,random_state=0,n_init=10)

#treinando o modelo
kmeans.fit(filmes_assistidos)

#Classificando os usuários
grupos_indice = kmeans.predict(filmes_assistidos)

#Exibir os dados
print("usuário pertence ao seguinte grupo: ")
for i, cluster in enumerate(grupos_indice):
  print(f"Usuário {i+1} pertence ao grupo {cluster}") #o i é de iteração

print("\nFilmes assistidos:")
for i in range (len(filmes_assistidos)):
  assistidos = np.where(filmes_assistidos[1]==1)[0] + 1
  print(f"usuário {i+1} assistiu aos filmes: {assistidos}")

# função que recomendar filmes
def recomendar_filmes(filmes, filmes_assistindo, grupos_indice):

  filmes = np.array(filmes)

  # Encontrar o grupo do usuário com base em seu vetor de filmes
  usuário_id = len(filmes_assistidos)
  grupo_usuario = kmeans.predict([filmes])[0]

  #Encontrar todos os usuários no mesmo grupo
  usuarios_no_mesmo_grupo = [i for i in range(len(grupos_indice))
  if grupos_indice[i] == grupo_usuario]

  # Filmes assistidos pelos usuários do mesmo grupo
  filmes_recomendados = set()
  for usuario in usuarios_no_mesmo_grupo:
    filmes_assistidos_usuario = np.where(filmes_assistidos[usuario] == 1)[0]
    filmes_recomendados.update(filmes_assistidos_usuario)

  # Remover filmes que o usuário já assistiu
  filmes_recomendados = filmes_recomendados - set(np.where(filmes == 1)[0])

  # Ajustar os ìndices dos filmes recomendados (de volta para 1-based)
  filmes_recomendados = [filme + 1 for filme in filmes_recomendados]

  return sorted(filmes_recomendados)

# exemplo de uso da função recomendar_filmes
filmes_assistidos_usuario = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] #vetor de filmes
 #assistidos (por exemplo, assistiu ao filme 1 e 3)
filmes_recomendados = recomendar_filmes (filmes_assistidos_usuario, filmes_assistidos, grupos_indice)

print(f"\nFilmes recomendados: {filmes_recomendados}")