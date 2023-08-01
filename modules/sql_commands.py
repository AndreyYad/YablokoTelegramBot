from sqlite3 import connect

class sql_commands():
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