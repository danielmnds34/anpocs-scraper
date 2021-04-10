"""Código para a aquisição dos dados dos Encontros Anuais da ANPOCS."""
from bs4 import BeautifulSoup
import pandas as pd
import re
from tqdm import tqdm
from helium import (
    start_chrome, click, get_driver, kill_browser, find_all, S
)

URL = ("https://www.anpocs2020.sinteseeventos.com.br/atividade/view?q=YToyOnt"
       "zOjY6InBhcmFtcyI7czozNjoiYToxOntzOjEyOiJJRF9BVElWSURBREUiO3M6MzoiMTI2"
       "Ijt9IjtzOjE6ImgiO3M6MzI6ImZjMjI3ODMwZTkzOTlmYjg1NzNjM2Y0MTUzNTM0NTEzI"
       "jt9&ID_ATIVIDADE=126")

def get_urls(base_url):
    pass

def get_page_source(url):
    """Obtém código-fonte completo da página."""
    # inicia o chrome para renderizar o código-fonte 
    start_chrome(url, headless=True)

    # clica em todos os botões "Veja mais!" para liberar os dados dos resumos
    print("Clicando em todos os botões. Isso pode demorar alguns segundos...")
    buttons = find_all(S("//span[@onClick]"))
    for i in tqdm(range(len(buttons))):
        click("Veja mais!")
        print(f"\nClique número {i}: um resumo aberto...")
    print('Fim dos cliques. Todos os resumos estão disponíveis.')

    # obtém objeto soup a partir do código-fonte renderizado pelo helium
    driver = get_driver()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # fecha o chrome
    kill_browser()

    return soup

def get_data(soup):
    """Obtém dados dos trabalhos apresentados."""
    # obtém dados textuais a partir dos seletores CSS de cada campo 
    authors = [autor.text for autor in soup.select('i')]
    titles = [titulo.text for titulo in soup.select('li > b')]
    abstract_source = soup.find_all('div', id=re.compile('^resumoFull'))
    abstracts = [abstract.text.strip() for abstract in abstract_source]

    # cria dict com os dados obtidos
    data = {
        'autores': authors,
        'titulo': titles,
        'resumo': abstracts
    }

    return data

if __name__ == "__main__":
    soup = get_page_source(url=URL)
    data = get_data(soup)
    df = pd.DataFrame(data)
    df.to_csv('anpocs_publications.csv', index=False)
