import psycopg2

try:
    conn = psycopg2.connect(dbname='db', user='postgres', password='pass', host='localhost', port=5432)
    print("Подключение успешно.")

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM cats')
    all_cats = cursor.fetchall()
    print(all_cats)
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print("Не удалось подключиться к базе данных.", e)

