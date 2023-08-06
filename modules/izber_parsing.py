from aiohttp import ClientSession
from json import loads, dump
from json.decoder import JSONDecodeError
from pprint import PrettyPrinter

import asyncio 

async def to_json(obj, name_file='output'):
    with open(f'{name_file}.json', 'w', encoding='utf-8') as file:
        dump(obj, file, indent=4, ensure_ascii=False)

async def cikrf(street, house):

    check_address = lambda orig, new: new == orig

    url = f'http://cikrf.ru/iservices/voter-services/address/search/Новгородская область, город Великий Новгород, {street}, {house}'

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

                uchastok_dict = loads(await address_info.text())

                uchastok_info = {
                    'num' : int(uchastok_dict['name'][-2:]),
                    'address' : uchastok_dict['votingAddress']['address']
                }

                return uchastok_info
            
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
            await to_json(streets)

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
                await to_json(houses)

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
                    await to_json(uchastok_dict)

                    uchastok_info = {
                        'num' : int(uchastok_dict['name'][-2:]),
                        'address' : uchastok_dict['address']
                    }

                    # print(uchastok_info)

                    return uchastok_info

async def izber_uchastok(street, house, only_mfc=False):
    house = house.replace(', корп. ', ' ').replace('д. ', '').lstrip().rstrip()
    street = street.lstrip().rstrip()

    print(f'прием - [{street},{house}]')
    cik_ver = await cikrf(street, house)
    if cik_ver == None or only_mfc:
        print('МФЦ')
        return await mfc(street, house)
    else:
        print('ЦИК')
        return cik_ver

if __name__ == '__main__':
    # 'Набережная Александра Невского', 'д. 22/2'
    street = 'Кочетова'
    house = '2 2'
    print(asyncio.run(izber_uchastok(street, house, only_mfc=False)))