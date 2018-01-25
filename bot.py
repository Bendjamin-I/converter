import requests
import misc
import re
from convert import convert
from convert import get_valut
from convert import get_btc
from convert import int_iz_str
from convert import fl_iz_str
from time import sleep
#-----------------------------------------------------------------------------------------
token = misc.token	#создаём переменную token и импортируем в нее из файла misc значение токена 
URL = 'https://api.telegram.org/bot' + token + '/'	#url для отправки сообщения 
global last_update_id	#глобальная переменная для проверки последнего обновления id
last_update_id = 0 
#-----------------------------------------------------------------------------------------
def get_updates():	#функция для создания json файла с последним обновлением
	url = URL + 'getupdates'	#url для получения обновления 
	r = requests.get(url)	#переменная с последними обновлениями(через requests)
	return r.json()	#возвращаем json файл с последними обновлениями
#-----------------------------------------------------------------------------------------
def get_message():	#функция для получения последнего chat id и text пользователя
	data = get_updates()	#присваеваем переменной функцию get_message(json файл)
	last_object = data['result'][-1]	#присваеваем переменной последний результат(последний объект)
	current_update_id = last_object['update_id']	#присваеваем переменной последний update_id (update_id)
	global last_update_id	#указываем на глобальную переменную last_update_id
	if last_update_id != current_update_id:	#условный оператор проверки last_update_id
		last_update_id = current_update_id	#присвоение последнего update_id
		chat_id = last_object['message']['chat']['id']	#'выдираем' chat_id
		message_text = last_object['message']['text']	#'выдираем' text
		message = {'chat_id' : chat_id,	#записываем в переменную значения chat_id и text
				   'text' : message_text}
		return message	#если последние id не равны возвращаем переменную с chat_id и text
	return None	#если последний id равен настоящему то ничего не возвращаем 
#-----------------------------------------------------------------------------------------
def send_message(chat_id, text = 'Пожалуйста, подождите...'):	#функция для отправки сообщения 
	url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)	#url для отпраки сообщения 
	requests.get(url)	#отправка сообщения
#-----------------------------------------------------------------------------------------
def opr_valut(text, kol = 1):
	if 'биткоин' in text.lower():
		return get_btc(kol)
	if 'доллар' in text.lower():
		return get_valut('USD',kol)	
	if 'евро' in text.lower():
		return get_valut('EUR',kol)
	if 'грив' in text.lower():
		return get_valut('UAH',kol)
	else:
		return 'Что-то пошло не так...'
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
def main():	#основная функция
	while True:	#бесконечный цикл для обновления запросов
		answer = get_message()	#помещение функции с chat_id и text в переменную
		if answer != None:	#если get_message не вернула none то
			chat_id = answer['chat_id']	#выдираем chat_id
			text = answer['text']	#выдираем text
			if 'курс' in text.lower():
				send_message(chat_id,opr_valut(text))
			elif re.findall('(\d+)', text) != '':
				try:
					if ',' in text:
						kol = fl_iz_str(text)
					else:
						kol = int_iz_str(text)
					send_message(chat_id,opr_valut(text, kol))
				except IndexError:
					send_message(chat_id, 'Что-то пошло не так...')
			else:
				send_message(chat_id,"WTF??")
		else:	#если get_message вернула none то
			continue	#продолжаем цикл
		sleep(2)	#спим 2 секунды что бы не сильно спамить сервер
if __name__ == '__main__':	#стандарт
	main()	#стандарт