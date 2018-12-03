import pandas as pd
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver

docentes = pd.read_csv('docentes.csv', sep=';')

base_url = 'https://sigaa.ufrn.br/sigaa/public/docente/portal.jsf?siape='

ff = webdriver.Firefox()

lista = []

for index, row in docentes.iterrows():
    url = base_url + str(row['siape'])
    ff.get(url)
    page = bs(ff.page_source, 'html.parser')
    titulos = page.find('div', {'id':'formacao-academica'}).find_all('dt')
    titulos = [titulo.text.strip() for titulo in titulos]
    data_local = page.find('div', {'id':'formacao-academica'}).find_all('dd')
    data_local = [dl.text.strip() for dl in data_local]
    dados = dict(zip(titulos, data_local))
    dados['nome'] = row['nome']
    dados['locacao'] = row['locacao']
    lista.append(dados)

with open('output.json', 'w') as file:
    
    for data in lista:
        json.dump(data, file)
        file.write('\n')

    file.flush()
    file.close()
