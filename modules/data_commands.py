from modules.sql_commands import sql_commands
from modules.izber_parsing import izber_uchastok

class data():
    # Создание таблиц
    def born_of_tables():
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS users (id int primary key, status varchar(50))')
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS bot_msg (msg_id int primary key, id int)')
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS pre_reg (id int primary key, name varchar(50), address varchar(100), phone varchar(12))')
        sql_commands.change_in_table('yabloko', 'CREATE TABLE IF NOT EXISTS voters (id int primary key, name varchar(50), address varchar(100), phone varchar(12))')

    # Удаление пред регистрационых данных
    def delete_pre_reg(id):
        sql_commands.change_in_table('bot', 'DELETE FROM pre_reg WHERE id == \'%d\'' % (id))

    # Удаление данных пользователя из бд
    def delete_voter_data(id):
        sql_commands.change_in_table('yabloko', 'DELETE FROM voters WHERE id == \'%d\'' % (id))

    # Информация об участке и кандидате округа
    def uchastok_info(street, house):
        izber_info = { 'uchastok' : '', 'candidate' : '' }

    # Преобразование текста в адрес
    def text_to_address(text):
        address = {
            'street' : '',
            'house' : '',
            'korp' : ''
        }

        print(text)

        if data.check_text_address(text):
            text = text.split(',')
            address['street'] = text[0]
            address['house'] = text[1].replace(' д. ', '')
            if len(text) == 3:
                address['korp'] = text[2].replace(' корп. ', '')
        else:
            address = None

        return address

    # Проверка текста на прописание адреса
    def check_text_address(text):

        result = False

        if text.count(',') in [1,2]:
            text = text.split(',')
            if text[1].startswith(' д. ') and len(text[1]) > 4:
                if len(text) == 3:
                    if text[2].startswith(' корп. ') and len(text[2]) > 7:
                        result = True
                elif len(text) == 2:
                    result = True

        return result

if __name__ == '__main__':
    text = 'Кочетова, д. 2'
    print(data.text_to_address(text))