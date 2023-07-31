from sqlite3 import connect

class sql_commands():
    # Изменения в таблице
    def change_in_table(cmd):

        conn = connect('data/yabloko_tables.sql')
        cur = conn.cursor()

        cur.execute(cmd)
        conn.commit()

        cur.close()
        conn.close()

    # Получение статуса пользователя
    def check_status(id):

        conn = connect('data/yabloko_tables.sql')
        cur = conn.cursor()

        cur.execute('SELECT status FROM users WHERE id = \'%d\'' % (id))
        result = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        return result