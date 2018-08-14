import sqlite3
conn = sqlite3.connect('desafio.db')
c = conn.cursor()
c.execute("create table funcionarios (id integer primary key autoincrement, idade int, nome text, cargo text)")
c.execute("create table acoes (id integer primary key autoincrement, metodo text, retorno text, data_hora text)")
conn.commit()
conn.close()
print("Base de dados configurada com sucesso.")