from sqlite3 import connect

class sql_commands():
    # Создание таблиц
    def born_of_tables():
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS users (id int primary key, status varchar(50))')
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS bot_msg (msg_id int primary key, id int)')
        sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS pre_reg (id int primary key, name varchar(50), address varchar(100))')
        sql_commands.change_in_table('yabloko', 'CREATE TABLE IF NOT EXISTS voters (id int primary key, name varchar(50), address varchar(100))')

    # Изменения в таблице
    def change_in_table(file_name, cmd):

        conn = connect(f'data/{file_name}_tables.sql')
        cur = conn.cursor()

        cur.execute(cmd)
        conn.commit()

        cur.close()
        conn.close()

    # Получить историю сообщений бота
    def history_bot_msg(id):

        conn = connect('data/bot_tables.sql')
        cur = conn.cursor()

        cur.execute('SELECT msg_id FROM bot_msg WHERE id = \'%d\'' % (id))
        
        result = []

        for msg in cur.fetchall():
            result.append(msg[0])

        cur.close()
        conn.close()

        return result
    
    # Очистить историю сообщений бота
    def clear_history_bot_msg(msg_id):

        conn = connect('data/bot_tables.sql')
        cur = conn.cursor()

        cur.execute('DELETE FROM bot_msg WHERE msg_id == \'%d\'' % (msg_id))
        conn.commit()

        cur.close()
        conn.close()

    # Получение статуса пользователя
    def check_status(id):

        conn = connect('data/bot_tables.sql')
        cur = conn.cursor()

        cur.execute('SELECT status FROM users WHERE id = \'%d\'' % (id))
        result = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        return result

    # Смена статуса пользователя
    def set_status(id, status):

        conn = connect('data/bot_tables.sql')
        cur = conn.cursor()

        cur.execute('UPDATE users SET status = \'%s\' WHERE id = \'%d\'' % (status, id))
        conn.commit()

        cur.close()
        conn.close()