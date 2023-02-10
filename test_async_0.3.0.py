import tkinter as tk
from tkinter import VERTICAL, Entry, ttk, Label
import random
import requests
import json
from call_main import call_api
from db_main_buy import update_inform_db, delete_string_where
from db_order_buy import update_inform_db_order
from bs4 import BeautifulSoup as bs

"""
не открывать пока не настроишь купленный прокси
Это для бесплатных прокси, не работает!!! просто как напоминание 
Удалить что бы не мешал!

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies
free_proxies = get_free_proxies()

def get_session(free_proxies):
    # создать HTTP‑сеанс
    session = requests.Session()
    # выбираем один случайный прокси
    proxy = random.choice(free_proxies)
    session.proxies = {"http": proxy, "https": proxy}
    return session

for i in range(5):
    s = get_session(free_proxies)
    try:
        print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
    except Exception as e:
        continue
"""

class Application(tk.Frame):
	def __init__(self, window):
		self.window = window 
		self.initialize_user_interface()
		self.window.resizable(height = False, width = False)
		self.avto_add_taible_in_bd()


	def initialize_user_interface(self):  #  Рисует таблицы, кнопки, вводы данных доп информацию
		self.window.title("Bot yobit")
		self.window.geometry('1000x700')

		self.entry_pair = Entry(self.window, width=15)
		self.lable_pair = Label(self.window, text='Валютная пара:')
		self.entry_pair.place(x=130, y=35)
		self.lable_pair.place(x=10, y=35)		

		self.entry_coin = Entry(self.window, width=15)
		self.lable_coin = Label(self.window, text='На какую сумму:')
		self.lable_coin.place(x=10, y=55)
		self.entry_coin.place(x=130, y=55)
		
		#  Кнопки и виждеты 
		self.button_add_online = tk.Button(text='Добавить',
									width=8,
									bg='red',
									fg='white',
									command=self.insert_data_online).place(x=430, y=60)
		self.button_buy = tk.Button(text='Купить',
									width=8,
									bg='green',
									fg='yellow',
									command=self.pair_buy).place(x=255, y=30)
		self.button_order = tk.Button(text='Купить ордер',
									width=13,
									bg='orange',
									fg='black',
									command=self.order_buy_yobit).place(x=325, y=30)
		self.button_order = tk.Button(text='Продать ордер',
									width=13,
									bg='orange',
									fg='black',
									command=self.order_sell_yobit).place(x=325, y=90)
		self.button_sell = tk.Button(text='Продать',
									width=8,
									bg='red',
									fg='black',
									command=self.pair_sell).place(x=430, y=30)
		self.button_order_pass = tk.Button(text='Отменить ордер',
									width=13,
									bg='blue',
									fg='black',
									command=self.order_pass).place(x=325, y=60)
		self.button_delete_teible = tk.Button(text='Удалить',
									width=8,
									bg='black',
									fg='red',
									command=self.delete_focus).place(x=610, y=440)


		#  Создание таблицы снизу, для купленных либо выставленных пар 
		columns = ('buy_sel', 'amount', 'type', 'ID order')
		self.tree1 = ttk.Treeview(self.window, columns=columns, height=20)
		self.tree1.place(height=225, width=982, rely=0.68)
		self.tree1.column("#0", width=150, minwidth=200)
		self.tree1.column("buy_sel", width=150, minwidth=150)
		self.tree1.column("amount", width=150, minwidth=200)
		self.tree1.column("type", width=150, minwidth=50)
		self.tree1.column("ID order", width=150, minwidth=120)
		self.tree1.heading("#0", text='Валютная пара', anchor=tk.W)
		self.tree1.heading("buy_sel", text="Цена покупки/продажи", anchor=tk.W)
		self.tree1.heading("amount", text="Количетво монет", anchor=tk.W)
		self.tree1.heading("type", text='Тип ордера', anchor=tk.W)
		self.tree1.heading("ID order", text='ID order', anchor=tk.W)
		self.ysb = ttk.Scrollbar(self.window, orient=VERTICAL, command=self.tree1.yview)
		self.tree1.configure(yscroll=self.ysb.set)
		self.ysb.place(x=980, y=480, height=220)


		#  Создание таблицы справа, для онлайн пар
		columns = ('Buy', 'Sell', 'Persent')
		self.tree = ttk.Treeview(self.window, columns=columns, height=20)
		self.tree.column("#0", width=70, minwidth=70, stretch=tk.YES)
		self.tree.column("Buy", width=85, minwidth=85)
		self.tree.column("Sell", width=85, minwidth=85)
		self.tree.column("Persent", width=45, minwidth=45)
		self.tree.heading('#0', text='Pair')
		self.tree.heading("Buy", text='Buy')
		self.tree.heading("Sell", text='Sell')
		self.tree.heading('Persent', text='Persent')
		self.tree.place(height=430, width=300, relx=0.681, rely=0.06)

		self.ysb = ttk.Scrollbar(self.window, orient=VERTICAL, command=self.tree.yview)
		self.tree.configure(yscroll=self.ysb.set)
		self.ysb.place(x=979, y=41, height=430)

		self.treeview = self.tree
		self.iid = 0

		self.treeview1 = self.tree1
		self.id = 0

	def avto_add_taible_in_bd(self):
		"""Функция которая при включении бота, из БД добавляет в таблицу снизу все валютные пары которые куплены
		и проверяет есть ли они на балансе """
		pass

	def insert_data_online(self): #  Добовляет в таблицу случайную валютную пару, 
		with open('pair.txt', 'r') as file:
			pairs = file.readlines()
		i = random.choice(pairs)
		pair = i.replace('\n', '')
		pair = pair.replace(' ', '')
		res = requests.get("https://yobit.io/api/3/depth/"+pair+'?limit=150')
		print(res)
		print(pair)
		list_price = json.loads(res.text)
		asks = list_price[pair]['asks'][0][0]
		bids = list_price[pair]['bids'][0][0]
		percent = (asks / bids) * 100
		self.treeview.insert('', 'end', iid=self.iid, text=pair , values=(asks, bids, percent)) 
		self.iid = self.iid + 1 


	def pair_buy(self):  #  После нажатия кнопки купить, ,берет значение из введеных пары и сумму на которую нужно купить, запсывает в таблицу внизу и в БД
		res = requests.get('https://yobit.io/api/3/depth/' + self.entry_pair.get() + '?limit=150')
		if res.status_code == 200:
			list_price = json.loads(res.text)
			asks = list_price[self.entry_pair.get()]['asks'][0][0]
			amount_coin = float(self.entry_coin.get()) / asks
			list_bye = call_api(method="Trade", pair=self.entry_pair.get(), type="buy", rate=asks, amount=amount_coin)
			print(list_bye)
			order_id = list_bye['return']['order_id']
			update_inform_db(self.entry_pair.get(), asks, amount_coin, 'buy', order_id)
			self.treeview1.insert('', 'end', iid = self.id, text = self.entry_pair.get(), values = (asks, amount_coin, 'buy', order_id))
			self.id = self.id + 1
		else:
			print(res.status_code)

	def pair_sell(self):   #  Продает выбраную валютную пару, и выбраное колличество монет по цене рынка. Так же удаляет из таблицы снизу запись и из БД
		res = requests.get('https://yobit.io/api/3/depth/' + self.entry_pair.get() + '?limit=150')
		if res.status_code == 200:
			list_price = json.loads(res.text)
			bids = list_price[self.entry_pair.get()]['bids'][0][0]		
			call_api(method="Trade", pair=self.entry_pair.get(), type="sell", rate=bids, amount=self.entry_coin.get())
			delete_string_where(self.entry_pair.get())
			
	def order_buy_yobit(self):
		"""Берет валютную пару из Ентри, выставляет ордер по цене продажи можно -1 сатош, 
		добавляет в таблицу снизу и в БД """
		res = requests.get('https://yobit.io/api/3/depth/' + self.entry_pair.get() + '?limit=150')
		if res.status_code == 200:
			list_price = json.loads(res.text)
			bids = list_price[self.entry_pair.get()]['bids'][0][0]
			amount_coin = float(self.entry_coin.get()) / bids
			list_bye = call_api(method="Trade", pair=self.entry_pair.get(), type="buy", rate=bids+0.00000001, amount=amount_coin)
			order_id = list_bye['return']['order_id']
			update_inform_db_order(self.entry_pair.get(), bids, amount_coin, 'order_buy', order_id)
			self.treeview1.insert('', 'end', iid = self.id, text = self.entry_pair.get(), values = (bids, amount_coin, 'order_buy', order_id))
			self.id = self.id + 1
		else:
			print(res.status_code)

	def order_sell_yobit():
		"""Берет валютную пару из Ентри, если только есть в кпленных парах , выставляет ордер по цене покупки  можно +1 сатош, 
		добавляет в таблицу снизу и в БД """
		res = requests.get('https://yobit.io/api/3/depth/' + self.entry_pair.get() + '?limit=150')
		if res.status_code == 200:
			list_price = json.loads(res.text)
			asks = list_price[self.entry_pair.get()]['asks'][0][0]
			list_bye = call_api(method="Trade",
								pair=self.entry_pair.get(),
								type="sell", 
								rate=asks-0.00000001, 
								amount=self.entry_coin.get())
			order_id = list_bye['return']['order_id']
			update_inform_db_order(self.entry_pair.get(), asks, self.entry_coin.get(), 'order_sell', order_id)
			self.treeview1.insert('', 'end', iid = self.id, text = self.entry_pair.get(), values = (asks, self.entry_coin.get(), 'order_sell', order_id))
			self.id = self.id + 1

	def order_pass():
		"""Нужно добавить автоматическое удаление из таблицы снизу после отмены ордера"""
		list_bye = call_api(method="CancelOrder",
							order_id=self.entry_coin.get())
		delete_string_where_order(self.entry_pair.get())


	def delete_focus(self):
		"""нужно переписать функцию что бы удалялась строка после продажи валютной пары т.е. нажатия на кнопку продать,
		суйчас нужно вбрать нужную строку что бы ее удалить кнопкой Удалить"""
		row_id = self.tree1.focus()
		self.treeview1.delete(row_id)



app = Application(tk.Tk())

app.window.mainloop()


