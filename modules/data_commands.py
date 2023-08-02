from modules.sql_commands import sql_commands

class data():
    # Создание таблиц
    def born_of_tables():
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS users (id int primary key, status varchar(50))')
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS bot_msg (msg_id int primary key, id int)')
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS pre_reg (id int primary key, name varchar(50), address varchar(100))')
        sql_commands.change_in_table('yabloko', 'CREATE TABLE IF NOT EXISTS voters (id int primary key, name varchar(50), address varchar(100))')

    # Удаление пред регистрационых данных
    def delete_pre_reg(id):
        sql_commands.change_in_table('bot', 'DELETE FROM pre_reg WHERE id == \'%d\'' % (id))

    def delete_voter_data(id):
        sql_commands.change_in_table('yabloko', 'DELETE FROM voters WHERE id == \'%d\'' % (id))