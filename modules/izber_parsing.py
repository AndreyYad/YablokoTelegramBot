from requests import get
from json import loads

def izber_uchastok(street, house):
    if '/' in house:
        house = house.split('/')
        try:
            house = house[0] + house[1][house[1].index(','):]
        except ValueError:
            house = house[0]

    url = f'http://cikrf.ru/iservices/voter-services/address/search/Новгородская область, город Великий Новгород, {street}, {house}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    }

    server = get(url, headers=headers)
    output = loads(server.text)

    try:
        if ' кв. ' in output[0]['name']:
            return None

        district_id = output[0]["id"]
    except IndexError:
        return None

    address_info = get(f"http://cikrf.ru/iservices/voter-services/committee/address/{district_id}", headers=headers)

    uchastok_dict = loads(address_info.text)

    # print(uchastok_dict)

    uchastok_info = {
        'num' : int(uchastok_dict['name'][-2:]),
        'address' : '{},{}'.format(uchastok_dict['votingAddress']['address'], uchastok_dict['votingAddress']['descr'])
    }

    return uchastok_info

if __name__ == '__main__':
    print(izber_uchastok('Набережная Александра Невского', 'д. 22/2'))