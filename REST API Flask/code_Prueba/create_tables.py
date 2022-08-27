import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (_id text, name text, apellido text, cedula text, fecha_nacimiento text)"
cursor.execute(create_table)

create_users = "INSERT INTO users VALUES ('1', 'Robert', 'Ortega', '94040558', '1982-07-06 00:00:00.000')"
cursor.execute(create_users)
create_users = "INSERT INTO users VALUES ('2','Prueba', 'Prueba', '94040557', '1980-07-06 00:00:00.000')"
cursor.execute(create_users)

connection.commit()
connection.close()