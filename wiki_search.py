import requests

from bs4 import BeautifulSoup

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

weapon = input('Weapon Name: ')

# -------------------------------------------------------------------------------------------------------------- Парсит html код с сайта и делает из него суп
def request_data(url):
   a = requests.get(url, headers=HEADERS).text
   return BeautifulSoup(a, 'html.parser')



# -------------------------------------------------------------------------------------------------------------- Создает шаблон ссылки для поиска
def wiki_search_content_url():
   return 'https://warframe.fandom.com/wiki/Special:Search?query='+weapon



# -------------------------------------------------------------------------------------------------------------- Ищет ссылку на страницу на английской Вики
def wikipage_link_finder():

   data = request_data(
      wiki_search_content_url()
   )

   return data.find('li', class_='unified-search__result').find('a').get('href')