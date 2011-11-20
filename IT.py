import sys, os,mysql.connector,time,datetime

def main():
	config={'use_unicode': True,
		'database': '',
		'charset': 'utf8',
		'host': '',
		'get_warnings': True,
		'user': '',
		'password': '',
		'port': 3306}
	db = mysql.connector.Connect(**config)
	cursor = db.cursor()
	while True:
		ans=what_to_do_stolb(('1.Замена картриджа','2.Новый актив'))
		if ans=='1':
			cartrige_change(cursor)
		ans=what_to_do(('Продолжить','Выйти'))
		if ans=='в': exit()



def cartrige_change(cursor):
	QUERY = "SELECT DISTINCT `Department` FROM `printer_department`"
	cursor.execute(QUERY)
	departments=[row[0] for row in cursor.fetchall()]
	now = datetime.datetime.now() 
	year, month, day, hour, minutes, sec, wday, yday, isdst = now.timetuple()  
	if month<10: month = "0%s" % month
	if day<10: day = "0%s" % day
	# запрос отдела
	while True:
		
		department=select(departments+['На уровень вверх',],'Выберите номер отдела [0]:')
		if department=='На уровень вверх': break
		QUERY = "SELECT `pd`.`Printer`,`a`.`Model` FROM `printer_department` `pd` INNER JOIN `assets` `a` ON `a`.`AssetNumber`=`pd`.`Printer` WHERE `pd`.`Department`='"+department+"' AND `pd`.`removed`='0000-00-00 00:00:00'"
		cursor.execute(QUERY)
		printers=[(row[0],row[1]) for row in cursor.fetchall()]
		#Выбор принтера
		while True:
			printer=select_with_name(printers+[('0','На уровень вверх')],'Выберите номер принтера [0]:',2)
			if printer[0]=='0': break
			# возвращается значение (номер, модель)
			# выборка имеющихся картриджей
			QUERY = "SELECT `a`.`AssetNumber` FROM `printer_cartridge_type` `pct` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`CartridgeType`=`pct`.`CartridgeType` INNER JOIN `assets` `a` ON `a`.`Model`=`cct`.`Model` WHERE `pct`.`Model`='"+printer[1]+"' AND `a`.`AssetCategoryNumber`=1 AND `a`.`StatusCode`=0"
			cursor.execute(QUERY)
			cartriges=[row[0] for row in cursor.fetchall()]
			if not cartriges:
				print ("Нет подходящих картриджей!")
				break
			while True:
				cartrige=select(cartriges+['На уровень вверх',],'Выберите номер картриджа [0]:')
				if cartrige=='На уровень вверх': break
				print ("Установить в принтер {0}<{1}> в отделе {3} картридж {2}?".format(printer[1],printer[0],cartrige,department))
				ans=what_to_do(('да','нет'))
				if ans=='y':
					QUERY = "UPDATE `assets` SET `StatusCode`=5 WHERE `AssetNumber`="+str(cartrige)
					cursor.execute(QUERY)
					print (QUERY)
					QUERY = "INSERT INTO `printer_cartridge`(`Printer`, `Cartridge`, `put`) VALUES ("+",".join((str(printer[0]),str(cartrige),"'"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))))+"')"
					cursor.execute(QUERY)
					print (QUERY)
				elif ans=='n':
					print ('Отмена задачи')

def what_to_do_stolb(tuple):
	ask="\n".join(["["+k[0].upper()+"]"+k[1:] for k in tuple])+"\n["+tuple[0][0].upper()+"]:"
	dop_ans={k[0].lower() for k in tuple}|{k[0].upper() for k in tuple}
	while True:
		ans=input(ask)
		if ans=='':
			return tuple[0][0].lower()
		if ans not in dop_ans:
			print("Ошибка! Допустимые варианты ответа:", str("".join(sorted(dop_ans,key=str.lower))))
		else:
			return ans.lower()
def what_to_do(tuple):
	ask=" ".join(["["+k[0].upper()+"]"+k[1:] for k in tuple])+" ["+tuple[0][0].upper()+"]:"
	dop_ans={k[0].lower() for k in tuple}|{k[0].upper() for k in tuple}
	while True:
		ans=input(ask)
		if ans=='':
			return tuple[0][0].lower()
		if ans not in dop_ans:
			print("Ошибка! Допустимые варианты ответа:", str("".join(sorted(dop_ans,key=str.lower))))
		else:
			return ans.lower()
def get_integer(message,default=None,min=0,max=100,allow_zero=True):
	try:
		default=int(default)
	except ValueError:
		print("Значение по умолчанию должно быть числом! Значение по умолчанию установлено в 0")
		default=0
	while True:
		try:
			result=input((message+":" if not default else message+" ["+str(default)+"]:"))
			if not result:
				if default:
					return default
				if allow_zero:
					return 0
			else:
				if not min<=int(result)<=max:
					print ("Число должно быть не меньше {0} и не больше {1}".format(min,max))
				else:
					return int(result)
		except ValueError:
			print("Вводимое значение по умолчанию должно быть числом")
def get_string(message,default=None,min=0,max=100,allow_zero=True):
	try:
		default=str(default)
	except ValueError:
		print("Значение по умолчанию должно быть строкой! Значение по умолчанию установлено в ''")
		default=''
	while True:
		result=input((message+":" if not default else message+" ["+default+"]:"))
		if not result:
			if default:
				return default
			if allow_zero:
				return ''
		else:
			if not min<len(result)<max:
				print ("Длина строки должна быть не меньше {0} и не больше {1}".format(min,max))
			else:
				return result
def select(tuple,msg):
	for k,v in enumerate(tuple):
		print ("{0:<{2}}.{1}".format(k,v,get_shirina_nomera(tuple)))
	dop_ans=set(str(k) for k in range(len(tuple)))
	while True:
		ans=input(msg)
		if ans=='':
			return tuple[0]
		elif ans not in dop_ans:
			print("Ошибка! Допустимые варианты ответа:", str(",".join(sorted(dop_ans,key=int))))
		else:
			return tuple[int(ans)]
def select_with_name(tuple,msg,count):
	for k,v in enumerate(tuple):
		print ("{0:<{2}}.{1:<{4}}...<{3}>".format(k,v[1],get_shirina_nomera(tuple),v[0],get_shirina_stolbza([j[1] for j in tuple])))
	dop_ans=set(str(k) for k in range(len(tuple)))
	while True:
		ans=input(msg)
		if count==1:
			if ans=='':
				return tuple[0][0]
			if ans not in dop_ans:
				print("Ошибка! Допустимые варианты ответа:", str(",".join(sorted(dop_ans,key=int))))
				continue
			else:
				return tuple[int(ans)][0]
		if count==2:
			if ans=='':
				return tuple[0][0],tuple[0][1]
			if ans not in dop_ans:
				print("Ошибка! Допустимые варианты ответа:", str(",".join(sorted(dop_ans,key=int))))
				continue
			else:
				return tuple[int(ans)][0],tuple[int(ans)][1]
def get_shirina_nomera(tuple):
	if len(tuple)<10:
		return 1
	elif len(tuple)<100:
		return 2
	else:
		return 3
def get_shirina_stolbza(tuple):
	len_max=0
	for k in tuple:
		if len(k)>len_max:
			len_max=len(k)
	return len_max

main()