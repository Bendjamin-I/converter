import re
import requests
#def otvet():
#	return None
rub = ' рублей'	#что бы не писать по несколько раз одно и тоже
usd = ' usd'	#что бы не писать по несколько раз одно и тоже
url = "http://www.cbr-xml-daily.ru/daily_json.js"	#сайт с которого берем курс (ЦБ)
#-----------------------------------------------------------------------------------------
response = requests.get(url).json()	#инвертируем сайт в json

#-----------------------------------------------------------------------------------------
god = (response['Date'])[:4]	#год
mes = (response['Date'])[5:7]	#месяц
chis = (response['Date'])[8:10]	#число
data = chis + '.' + mes + '.' + god	#собираем дату
uvedomlenie = ' По курсу ЦБ на ' + data	#уведомление откуда взят курс и на какую дату 
#-----------------------------------------------------------------------------------------
def convert(text):
	if ',' in text:
		chislo = fl_iz_str(text)
		
	else:
		chislo = int_iz_str(text)
	vChom = get_valut(v_chem(text))
	chego
	
		
def int_iz_str(text):
	chis = int(re.findall(r'\d+', text)[0])
	return chis
def fl_iz_str(text):
	check_text = re.split(r',',text)
	chis = re.findall(r'\d+',check_text[0]) + re.findall(r'\d+',check_text[1])
	fl = chis[0] + '.' + chis[1]
	return float(fl)
def v_chem(text):
	if 'в долларах' in text:
		return 'USD'
	if 'в евро' in text:
		return 'EUR'
	if 'в гривнах' in text:
		return 'UAH'
def get_valut(a, kol):	#доллар
	kol = float(kol)
	prise = response["Valute"]['{}'.format(a)]['Value']	#выдираем валюту
	result = uvedomlenie + '\n' + '\n' + str(kol*float(round(prise, 2))) + rub	#формируем результат
	
	return result
	
	
def get_btc(kol):	#биткоин
	url = 'http://yobit.net/api/2/btc_usd/ticker'
	response = requests.get(url).json()
	prise = response['ticker']['last']
	return str(kol * int(prise)) + ' usd'	
#print(convert('1,464645 drth drg fg'))
