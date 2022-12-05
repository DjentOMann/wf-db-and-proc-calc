import json
import os

from datetime import date, timedelta, datetime

from wiki_search import wikipage_link_finder, request_data

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}



def write_json_file(obj, path):
    folder, _ = os.path.split(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, mode="w", encoding="utf-8") as json_file:
        json.dump(obj, json_file, indent=4)
        print(f'File {path} has been written: {datetime.now().strftime("%d-%m %H:%M")}')

def read_json_file(path):
    if not os.path.exists(path):
        return 
    with open(path, encoding="utf-8") as json_file:
        print(f'File {path} has been read: {datetime.now().strftime("%d-%m %H:%M")}')
        return json.load(json_file)



# -------------------------------------------------------------------------------------------------------------- Парсит всю инфу об оружии
def weapon_data_html():
    return request_data(wikipage_link_finder()).find('aside', {'role':'region'})



# -------------------------------------------------------------------------------------------------------------- Создает словарь с инфой об оружии с сайта
def weapon_wiki_data_collector():

    weapon_data_save = weapon_data_html()
    weapon_data = {}

    weapon_name = weapon_data_save.find('h2', class_='pi-item pi-item-spacing pi-title pi-secondary-background').text
    weapon_data['Weapon Name'] = weapon_name

    update_date = str(date.today())
    weapon_data['Update Date'] = update_date

    weapon_data['Weapon Parameters'] = {}

    parameters = weapon_data_save.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color')

    for item in parameters:
        weapon_data['Weapon Parameters'][item.get('data-source')] = item.find('div', class_='pi-data-value pi-font').text
    


    damage_types = weapon_data_save.find_all('td', class_='pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing')
    
    for item in damage_types:
        weapon_data['Weapon Parameters'][item.get('data-source')] = item.text



    write_json_file(weapon_data,'warframe_dmg_cal\weapon_data')

    return weapon_data



# -------------------------------------------------------------------------------------------------------------- Обновляет инфу об оружии в БД, если последнее обновление было 7 дней и более назад
def weapon_database_updater():

    weapon_database_save = read_json_file('warframe_dmg_cal\weapon_database')
    weapon_data_save = weapon_wiki_data_collector()
    weapon_list = []

    for item in weapon_database_save:
        weapon_list.append(item['Weapon Name'])
    
    if weapon_data_save['Weapon Name'] not in weapon_list:
        weapon_database_save.append(weapon_data_save)
    
    for item in weapon_database_save: 
        if item['Weapon Name'] == weapon_data_save['Weapon Name'] and date.today() - date.fromisoformat(item['Update Date']) >= timedelta(7):
            weapon_database_save[weapon_database_save.index(item)] = weapon_data_save

    write_json_file(weapon_database_save, 'warframe_dmg_cal\weapon_database')