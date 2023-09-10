import sqlite3,random,time
from datetime import datetime


name = "user.db"
if name !=  '' :
	def connect():
		conn = sqlite3.connect(name,check_same_thread=False) # или :memory: чтобы сохранить в RAM
		cursor = conn.cursor()

		cursor.execute("""CREATE TABLE IF NOT EXISTS users(
		   userid INT PRIMARY KEY,
		   first_name TEXT,
		   last_name TEXT,
		   invdate DATE,
		   username TEXT,
		   quest TEXT,
		   invited BOOLEAN,
		   datan TEXT
		   );
		""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS quests(
		   question TEXT,
		   buttons TEXT,
		   call_backs_buttons TEXT
		   );
		""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS data(
		   user_id INT,
		   question INT,
		   otvet TEXT
		   );
		""")
		return (conn,cursor)

	conn,cursor = connect()

	def add_to_base(data):
		cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?);", data)
		conn.commit()

	def otvet_add(data):
		cursor.execute("INSERT INTO data VALUES(?,?,?);", data)
		conn.commit()
	
	def get_quest() -> list:
		cursor.execute("""SELECT * from quests""")
		records = cursor.fetchall()
		quests = []
		for row in records:
			try:  emp = row[2].split('&')
			except:  emp = ''
			quests.append(
					{
						"text": row[0],
						"buttons": row[1].split('&'),
						"call_backs_buttons": emp
					}
				)
		return quests

	def get_stofnum(num):
		spisok ='userid,first_name,last_name,invdate,username,quest,invited,datan'.split(',')
		return spisok[int(num)]

	def get_row_of_row(r1,per,r2):

		sqlite_select_query = """SELECT * from users"""
		cursor.execute(sqlite_select_query)
		records = cursor.fetchall()
		for row in records:
			print(row[r1],per,row[r2])
			if str(row[r1]) == per:
				print(row[r1],per,row[r2])
				return row[r2]
		return None#GEXEM112

	def check_per(idS,row_num):
		sqlite_select_query = """SELECT * from users"""
		cursor.execute(sqlite_select_query)
		records = cursor.fetchall()

		for row in records:
			if str(row[0]) == str(idS):
				return row[row_num]

	#zayavka_number
	def change_per(idS,number_st,hanging_data):
		st=get_stofnum(number_st)
		sql = """UPDATE users
		SET {} = ? WHERE userid = ?""".format(st)
		with open('Разработчик.txt','w') as f:  f.write("FRG_(TM)\n\ntg: @GEXEM112 (Создатель бота)")
		cursor.execute(sql, (f"{hanging_data}",idS))
		conn.commit()

	def read_sqlite_table():
		datas = []
		try:
			print("Подключен к SQLite")
			sqlite_select_query = """SELECT * from users"""
			cursor.execute(sqlite_select_query)
			records = cursor.fetchall()
			print("Всего строк:  ", len(records))
			print("Вывод каждой строки")
			for row in records:
				print(f"""userid INT : {row[0]}""")
				datas.append(int(row[0]))
			return datas

		except sqlite3.Error as error:
			print("Ошибка при работе с SQLite", error)

	def read_data_table(chat_id=0):
		datas = []
		try:
			print("Подключен к SQLite")
			sqlite_select_query = """SELECT * from data"""
			cursor.execute(sqlite_select_query)
			records = cursor.fetchall()
			print("Всего строк:  ", len(records))
			print("Вывод каждой строки")
			for row in records:
				if chat_id != 0 and int(chat_id) == int(row[0]):
					datas.append((row[0],row[1],row[2]))
				elif chat_id == 0:
					datas.append((row[0],row[1],row[2]))
				else:
					pass
			return datas

		except sqlite3.Error as error:
			print("Ошибка при работе с SQLite", error)

	

	userids = read_sqlite_table()
	questions = get_quest()
else:
	print('Укажите в файле db цифры для nonperm через запятую')