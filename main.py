import json,time
from datetime import datetime
import db

#bot = TeleBot('5678015048:AAH3wZuTc7-Wpao7UTUeQCqlwH5UGQ4t4nY')
from config import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

messages_list = []
ids = []

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



def get_quest(beggin: int) -> str:
	try:
		return db.get_quest()[beggin]
	except:
		return {"text":'Вы успешно прошли тестирование','buttons':['Отправить заявку'],"call_backs_buttons":['invite']}

def forma(liste: list) -> str:
	return liste["text"]


def generate_buttons(liste: list) -> list: #from get_quests
	print(liste,liste["buttons"])
	if liste["buttons"][0] != "text":
		keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
		for i in liste["buttons"]:
			call_back = liste["call_backs_buttons"][int(liste["buttons"].index(i))]
			keyboard.add(InlineKeyboardButton(f'{i}', callback_data=f"{call_back}"))
		return keyboard
		
	else:
		return types.InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(f'Бот ожидает сообщения', callback_data=f"cancel_text"))

def shifr(text,status=0) -> str: # 0 = crypt , 1 - decrypt
	return text

def send_submit(liste: list) -> bool:
	# user_id, number question , otvet
	db.change_per(int(liste[0]),5,int(liste[1])+1)

	db.otvet_add((
			liste[0],
			liste[2],
			
			shifr(liste[1])
		))
	




@dp.chat_join_request_handler()
async def start(message: types.ChatJoinRequest):
	# тут мы принимаем юзера в канал
	#await update.approve()
	# а тут отправляем сообщение
	if message.from_user.id not in db.userids:
		db.userids.append(message.from_user.id)
		db.add_to_base(
					(
						f"{message.from_user.id}",
						f"{message.from_user.first_name}",
						f"{message.from_user.last_name}",
						datetime.now(),
						f"{message.from_user.username}",
						"0",
						False,
						f"{message}"
					)
				)
	if db.check_per(message.from_user.id,6) == 'True':
		datan = json.loads(db.check_per(message.from_user.id,7))
		await bot.approve_chat_join_request(chat_id=datan["chat"]["id"],
		user_id=datan["from"]["id"])


	else:
		messages_list.append(message)
		ids.append(message.from_user.id)
		await bot.send_message(chat_id=message.from_user.id, text="Здравствуйте!\n\nВы подали заявку на вступление в группу проекта «Дронница».\n\nДля наиболее эффективного взаимодействия просим Вас ответить на несколько простых вопросов.")
		await bot.send_message(chat_id=message.from_user.id, text=forma(
					get_quest(
						int (
							db.check_per(message.from_user.id,5)
							)
						)
					),reply_markup=generate_buttons(get_quest(int(db.check_per(message.from_user.id,5))))
				)



@dp.message_handler(commands=['start'])
async def get_text1(message: types.Message):
	print(db.check_per(message.from_user.id,6))
	if db.check_per(message.from_user.id,6) == 'True':

		datan = json.loads(db.check_per(message.chat.id,7))

		await bot.approve_chat_join_request(chat_id=datan["chat"]["id"],
		user_id=datan["from"]["id"])
	else:
		messages_list.append(message)
		ids.append(message.from_user.id)
		await bot.send_message(chat_id=message.from_user.id, text=forma(
					get_quest(
						int (
							db.check_per(message.from_user.id,5)
							)
						)
					),reply_markup=generate_buttons(get_quest(int(db.check_per(message.from_user.id,5))))
				)

@dp.message_handler()
async def get_text(message: types.Message):
	if int(db.check_per(message.chat.id,5)) < 11:
		send_submit((
				message.chat.id,
				int(db.check_per(message.chat.id,5)) , 
				message.text
			))
		await bot.send_message(chat_id=message.chat.id, text=forma(
				get_quest(
					int (
						db.check_per(message.chat.id,5)
						)
					)
				),reply_markup=generate_buttons(get_quest(int(db.check_per(message.chat.id,5))))
			)
	else:
		await admin(message.chat.id)
		await bot.send_message(chat_id=message.chat.id,text='Ваша заявка на рассмотрении.')

	


def get_data_of(chat_id=0): # ->str or list
	datas = db.read_data_table(chat_id)
	if chat_id != 0:
		text_ = '🛎 Уведомление о новой заявке 👤\n\n'
		text_ += f'{db.check_per(chat_id,1)}'
		text_ += f' {db.check_per(chat_id,2)}\n'
		text_ += f'Date: {db.check_per(chat_id,3)}\n'
		text_ += f'@{db.check_per(chat_id,4)}\n\n'
		for row in datas:
			try:
				text_ += '| Вопрос: <i>{}</i>\n| Ответ: {}\n\n'.format(
					get_quest(int(row[2]))["text"],
					row[1]
				)
			except:
				pass
		return text_
	else:
		return datas

async def admin(chat_id_: int):
	print(chat_id_,admin_id)
	adm_keys = types.InlineKeyboardMarkup(resize_keyboard=True).add(
		InlineKeyboardButton(f'Принять', callback_data=f"inv_{chat_id_}"),
		InlineKeyboardButton(f'Отклонить', callback_data=f"ban_{chat_id_}")
		)
	await bot.send_message(chat_id=admin_id,text=get_data_of(int(chat_id_)),parse_mode='HTML',reply_markup=adm_keys)

@dp.callback_query_handler()
async def query(call):
	chat_id = int(call.message.chat.id)
	
	
	if call.data not in ['cancel_text','','invite'] and 'inv_' not in call.data and 'ban_' not in call.data:
		quest_now = get_quest(int(db.check_per(chat_id,5)))
		print(quest_now["call_backs_buttons"])
		send_submit((
				chat_id,
				int(db.check_per(chat_id,5)) , 
				quest_now["buttons"][int(quest_now["call_backs_buttons"].index(call.data))]
			))
		await bot.send_message(chat_id=chat_id, text=forma(
				get_quest(
					int (
						db.check_per(chat_id,5)
						)
					)
				),reply_markup=generate_buttons(get_quest(int(db.check_per(chat_id,5))))
			)
	elif call.data == 'invite':
		await admin(chat_id)

	elif 'inv_' in call.data:
		db.change_per(int(call.data.split('_')[1]),6,'True')
		datan = json.loads(db.check_per(int(call.data.split('_')[1]),7))
		await bot.approve_chat_join_request(chat_id=datan["chat"]["id"],
		user_id=datan["from"]["id"])

	elif 'del_' in call.data:
		datan = json.loads(db.check_per(int(call.data.split('_')[1]),7))
		await bot.declineChatJoinRequest(chat_id=datan["chat"]["id"],
		user_id=datan["from"]["id"])
		await bot.delete_message(message.chat.id, message.id)



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
	
