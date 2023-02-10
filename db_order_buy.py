import sqlite3 as sq


def all_pair_base_order():  #  Возвращает все строки в БД
		db = sq.connect('base_01.db')
		cur = db.cursor()
		list_base_pair = cur.execute('SELECT * FROM order_base')
		return list_base_pair

def search_db_pair_order(name): #  Возвращает True Если в базе есть такая пара 
	with sq.connect('base_01.db') as con:
		cur = con.cursor()
		list_info_table = cur.execute('SELECT * FROM order_base')
		for t in list_info_table:
			if t[0] == name:
				return True

def return_amount_db_order(name):  #  Возвращает список имя пары, цену, количество монет, тип_ордера, ID ордера
	with sq.connect('base_01.db') as con:
		cur = con.cursor()
		list_info_table = cur.execute('SELECT * FROM order_base')
		for t in list_info_table:
			if t[0] == name:
				return [t[0], t[1], t[2], t[3], t[4]]

def update_inform_db_order(pair, asks, amount, type_order, id_order):  #  Обновление информации в базе в запвисимости есть там пара уже или нет 
	with sq.connect('base_01.db') as con:
		cur = con.cursor()
		if search_db_pair_order(pair):
			cur.execute("UPDATE order_base SET name = ?1, asks = ?2, amount = ?3, type = ?4, id_order = ?5 WHERE  name = ?1",
						(pair, asks, amount + return_amount_db_order(pair)[2], type_order, id_order ))
			print(f'Данная пара есть {pair} обновленно, колличество {return_amount_db_order(pair)[2]}')
		else:
			cur.execute("INSERT INTO order_base VALUES(?, ?, ?, ?, ?)", (pair, asks, amount, type_order, id_order))
			print(f"Добавленная новая валютная пара {pair}")

def delete_string_where_order(pair): #  Удаляет строку переданной пары если есть в БД
		with sq.connect('base_01.db') as con:
			cur = con.cursor()

			delet_pair = ("""DELETE from order_base where name = ?1""")
			cur.execute(delet_pair, (pair, ))