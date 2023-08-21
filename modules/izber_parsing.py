from aiohttp import ClientSession
from json import loads, dump, load
from json.decoder import JSONDecodeError
from itertools import product
from loguru import logger

import asyncio 

try:
    from modules.logger import setup_logger
except ModuleNotFoundError:
    from logger import setup_logger

async def to_json(obj, name_file='output'):
    with open(f'{name_file}.json', 'w', encoding='utf-8') as file:
        dump(obj, file, indent=4, ensure_ascii=False)

async def list_registers(text):
    result = []
    text = text.lower().split(' ')
    list_comb = [''.join(item) for item in list(product('10', repeat=len(text)))]
    for comb in list_comb:
        new_text = ''
        for index in range(len(comb)):
            if comb[index] == '0':
                new_text += text[index] + ' '
            else:
                new_text += text[index].title() + ' '
        result.append(new_text[:-1])

    return result

async def cikrf(street, house):

    check_address = lambda orig, new: new == orig

    url = 'http://cikrf.ru/iservices/voter-services/address/search/Новгородская область, город Великий Новгород, {}, {}'.format(street, house.replace('/',''))

    logger.debug(f'ссылка поиска: {url}')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            server = response

            try:
                output = loads(await server.text())
            except JSONDecodeError:
                return None

            try:

                name_out = output[0]['name'].replace('Новгородская область, город Великий Новгород, ', '')
                if ' кв. ' in name_out:
                    name_out = name_out[:name_out.find(', кв.')]
                
                # print(f'[{street}, д. {house}]')
                # print(f'[{name_out}]')

                if f'{street}, д. {house}' != name_out:
                    return None


                district_id = output[0]["id"]
            except IndexError:
                return None
            
            async with session.get(f"http://cikrf.ru/iservices/voter-services/committee/address/{district_id}", headers=headers) as response:
                address_info = response

                try:
                    uchastok_dict = loads(await address_info.text())
                except JSONDecodeError:
                    return None

                return int(uchastok_dict['name'][-2:])
            
async def mfc(street, house):

    # print(f'[{street},{house}]')

    url = 'https://mfc.zone/rest/getCikLocations'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    }

    data = {
        'intid' : 135637827259064320000378637,
        'parentId' : 4744673537
    }

    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            streets = loads(await response.text())

            for street_ in streets:
                if street in street_['text']:
                    street_data = street_
                    break
            else:
                return None

            data = {
                'intid' : street_data['intid'],
                'parentId' : street_data['id']
            }

            async with session.post(url, headers=headers, data=data) as response:
                houses = loads(await response.text())

                for house_ in houses:
                    if house == house_['text']:
                        house_data = house_
                        break
                else:
                    return None
                
                data = {
                    'intid' : house_data['intid'],
                    'parentId' : house_data['id'],
                    'region': 'Новгородская область'
                }

                url = 'https://mfc.zone/rest/getCikPlace'
            
                async with session.post(url, headers=headers, data=data) as response:
                    uchastok_dict = loads(await response.text())
                    
                    if uchastok_dict == None:
                        return None

                    return int(uchastok_dict['name'][-2:])
                
async def check_full_streets(street):
    with open('data/full_streets.json', encoding='utf-8') as file:
        try:
            return load(file)[street]
        except KeyError:
            return None

async def izber_uchastok(street, house):

    setup_logger()

    house = house.replace(', корп. ', ' ').replace('д. ', '').lstrip().rstrip()
    street = street.lstrip().rstrip()

    logger.debug(f'поиск: {street}, {house}')

    cik_ver = await cikrf(street, house)
    if cik_ver != None:
        # print('ЦИК')
        return cik_ver
    else:
        for ver_street in await list_registers(street):
            cik_ver = await cikrf(ver_street, house)
            if cik_ver != None:
                # print('ЦИК')
                return cik_ver
    
    # print('Улица полностью')
    return await check_full_streets(street)

if __name__ == '__main__':
    # 'Набережная Александра Невского', 'д. 22/2'
    street = 'Технический проезд'
    house = '3'
    print(asyncio.run(izber_uchastok(street, house)))

    # print(asyncio.run(cikrf(street, house)))
    # print(asyncio.run(list_registers('ad add assds adsdsd')))