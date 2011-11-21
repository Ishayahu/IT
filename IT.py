import sys, os,mysql.connector,time,datetime

def main():
	config={'use_unicode': True,
		'database': 'it',
		'charset': 'utf8',
		'host': '',
		'get_warnings': True,
		'user': '',
		'password': '',
		'port': 3306}
	db = mysql.connector.Connect(**config)
	cursor = db.cursor()
	while True:
		ans=what_to_do_stolb(('1.Замена картриджа и списание','2.Новый актив','3.Заказ картриджей','4.Инвентаризация картриджей','5-.Работа со счетами','6-.Работа с заявками', '7.Отчет по бюджету','В.Выход'))
		if ans=='1':
			cartrige_change(cursor)
		elif ans=='2':
			new_active(cursor)
		elif ans=='3':
			what_2_by(cursor)
		elif ans=='4':
			invent_cartridge(cursor)

		elif ans=='7':
			budjet(cursor)
		elif ans=='в': exit()
		ans=what_to_do(('Продолжить','Выйти'))
		if ans=='в': exit()

def invent_cartridge(cursor):
	SELECT_WHAT_IS="SELECT `Model`,`AssetNumber` FROM `assets` WHERE `AssetCategoryNumber`=1 AND `StatusCode`=0 ORDER BY `Model`;"
	cursor.execute(SELECT_WHAT_IS)
	what_is=[row for row in cursor.fetchall()]
	file=open('invent.txt','w',encoding='utf8')
	for k in what_is:
		file.write("{0:.<{2}}...<{1}>".format(k[0],k[1],get_shirina_stolbza([z[0] for z in what_is]))+'\n')
	file.close()
	exit()
def what_2_by(cursor):
	SELECT_WHAT_IS="SELECT `ct`.`CartridgeType` FROM `assets` `a` INNER JOIN `cartridge_cartridge_type` `ct` ON `a`.`Model`=`ct`.`Model` WHERE `AssetCategoryNumber`=1 and `StatusCode`=0;"
	SELECT_WHAT_NEED="SELECT `pct`.`CartridgeType` FROM `printer_department` `p` INNER JOIN `assets` `a` ON `a`.`AssetNumber`=`p`.`Printer` INNER JOIN `printer_cartridge_type` `pct` ON `pct`.`Model`=`a`.`Model` WHERE `removed`='0000-00-00 00:00:00';"
	cursor.execute(SELECT_WHAT_IS)
	what_is=[row for row in cursor.fetchall()]
	#print what_is
	cursor.execute(SELECT_WHAT_NEED)
	what_need=[row for row in cursor.fetchall()]
	#print what_need
	what_to_by=[]
	for k in range(len(what_need)):
			if what_need[k] in what_is:
					del what_is[what_is.index(what_need[k])]
			else:
					what_to_by.append(what_need[k])
	# расчет средней цены и занесение ее в словарь
	price_dict={}
	for k in set(k[0] for k in what_to_by):
		QUERY="SELECT AVG(`Price`) FROM `assets` WHERE `AssetCategoryNumber`=1  AND `Price`<>0 AND `Model` IN (SELECT `cct`.`Model` FROM `cartridge_cartridge_type` `cct` WHERE `cct`.`CartridgeType` = '"+str(k)+"')"
		cursor.execute(QUERY)
		for k1 in cursor.fetchall():
			z= k1[0] if k1[0] else 0
			avg_price=float(z)
			price_dict[k]=avg_price
	summ=0
	print ('\n\n')
	for k in what_to_by:
			print ("{0:.<{1}}.....{2:<}".format(k[0],get_shirina_stolbza([z[0] for z in what_to_by]),price_dict.get(k[0],0)))
			summ+=float(price_dict.get(k[0],0))
	print ('Итог: ',summ)
	print ('\n\n')
def budjet(cursor):
		now = datetime.datetime.now() 
		year, month, day, hour, minutes, sec, wday, yday, isdst = now.timetuple()  
		if month<10: month = "0%s" % month  
		month=get_integer('Month',month,1,12,False)
		year=get_integer('Year',year,0,year,False)
		MethodOfPayment=what_to_do_stolb(('Cash','NonCash')).upper()
		if MethodOfPayment=='N': MethodOfPayment='NC'
		QUERY = "SELECT `AssetCategoryNumber`, `Name` FROM `assetcategory`"
		cursor.execute(QUERY)
		TMP=[(row[0],row[1]) for row in cursor.fetchall()]
		# номер категории, название категории
		acat=dict([(k[0], k[1]) for k in TMP])
		QUERY = "SELECT `ByeDate`, `Price`, `Model`, `BillNumber`, `AssetCategoryNumber` FROM `assets` WHERE `ByeDate` < '"+str(year)+"-"+str(month+1)+"-01' AND `ByeDate` >= '"+str(year)+"-"+str(month)+"-01' AND `MethodOfPayment`='"+MethodOfPayment+"' ORDER BY `ByeDate` ASC"
		cursor.execute(QUERY)
		TMP=[row for row in cursor.fetchall()]
		file=open('budjet.csv','w',encoding='utf8')
		file.write('Дата;Расход;Остаток;На что;Чек;Категория\n')
		summ=25000
		for k in TMP:
			summ=summ-int(k[1])
			file.write(','.join((str(k[0]),str(k[1]),str(summ),str(k[2]),str(k[3]),acat[k[4]]))+'\n')
		QUERY = "SELECT `BillDate`, `Price`, `Breakdown`, `BilNumber` FROM `repairing` WHERE `BillDate` < '"+str(year)+"-"+str(month+1)+"-01' AND `BillDate` >= '"+str(year)+"-"+str(month)+"-01' AND `MethodOfPayment`='"+MethodOfPayment+"' ORDER BY `BillDate` ASC"
		cursor.execute(QUERY)
		TMP=[row for row in cursor.fetchall()]
		for k in TMP:
			summ=summ-int(k[1])
			file.write(','.join((str(k[0]),str(k[1]),str(summ),str(k[2]),str(k[3]),'Ремонт'))+'\n')
		file.close()
def new_active(cursor):
	now = datetime.datetime.now() 
	year, month, day, hour, minutes, sec, wday, yday, isdst = now.timetuple()  
	if month<10: month = "0%s" % month
	if day<10: day = "0%s" % day
	QUERY="SELECT `AssetCategoryNumber`, `Name` FROM `assetcategory`"
	cursor.execute(QUERY)
	categories=[(row[0],row[1]) for row in cursor.fetchall()]
	# номер категории, название категории
	while True:
		category=select_with_name(categories+[('В','На уровень вверх')],'Выберите номер принтера [0]:',2)
		if category[0]=='В': break
		models=[]
		if category[0]==0: # получить список моделей принтера
			QUERY="SELECT `Model`, COUNT(`Model`) FROM `assets` WHERE `AssetCategoryNumber`=0 AND `StatusCode`<>5 GROUP BY `Model` ORDER BY COUNT(`Model`) DESC"
			cursor.execute(QUERY)
			models=[row[0] for row in cursor.fetchall()]
		if category[0]==1: # получить список моделей картриджей
			QUERY="SELECT `Model`, COUNT(`Model`) FROM `assets` WHERE `AssetCategoryNumber`=1 GROUP BY `Model` ORDER BY COUNT(`Model`) DESC"
			cursor.execute(QUERY)
			models=[row[0] for row in cursor.fetchall()]
		while True:
			model=select(models+['На уровень вверх',],'Выберите модель актива: ',selfname=True)
			if model=='На уровень вверх': break
			while True:
				SerialNumber=get_string('Введите серийный номер актива',default='',min=0,max=100,allow_zero=True)
				StatusCode=select_with_name([(0,'Новое'),(1,'Б/У'),(2,'Глючное'),(3,'Не рабочее'),(4,'Возврат по гарантии'),(5,'Списано')],'Выберите статус актива [0]:',2)
				Garanty=get_integer('Введите срок гарантии',default=0,min=0,max=999,allow_zero=True)
				BillNumber=get_string('Введите номер чека',default='',min=0,max=100,allow_zero=False)
				QUERY="SELECT `d`.`DistributorName` FROM `distributors` `d` INNER JOIN `assets` `a` ON `a`.`DistributorName`=`d`.`DistributorName` GROUP BY `d`.`DistributorName` ORDER BY COUNT(`a`.`DistributorName`) DESC"
				cursor.execute(QUERY)
				distributers=[row[0] for row in cursor.fetchall()]
				DistributorName=select(distributers,'Выберите поставщика [0]: ')
				Price=get_float('Введите цену актива',default=0,min=0,max=25000,allow_zero=True)
				MethodOfPayment=what_to_do_stolb(('Cash','NonCash')).upper()
				if MethodOfPayment=='N': MethodOfPayment='NC'
				GarantyNumber=get_integer('Введите номер гарантии',default=0,min=0,max=999,allow_zero=True) if Garanty else 0
				QUERY="INSERT INTO `assets`(`AssetNumber`, `AssetCategoryNumber`, `Model`, `SerialNumber`, `StatusCode`, `Place`, `PCName`, `ByeDate`, `Garanty`, `Notes`, `Price`, `DistributorName`, `BillNumber`, `MethodOfPayment`, `GarantyNumber`, `CancellationDate`) VALUES ("+",".join(('null',str(category[0]),"'"+model+"'",("'"+SerialNumber+"'" if SerialNumber else "''"),str(StatusCode[0]), "'Склад'", 'null', "'"+"-".join((str(year),str(month),str(day)))+"'", str(Garanty), 'null', str(Price), "'"+DistributorName+"'", BillNumber, "'"+MethodOfPayment+"'", str(GarantyNumber), "'0000-00-00'"))+")"
				#print (QUERY)
				cursor.execute(QUERY)
				# вернуть введенный номер
				QUERY="SELECT MAX(`AssetNumber`) FROM `assets`"
				cursor.execute(QUERY)
				number=[row[0] for row in cursor.fetchall()][0]
				print ("Номер актива: ",number)
				break
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
		# Обработать списание картриджей
		if department=='Списание':
			while True:
				# выбираем картридж
				QUERY = "SELECT `AssetNumber` FROM `assets` WHERE `AssetCategoryNumber`=1 AND `StatusCode`=0"
				cursor.execute(QUERY)
				cartriges=[row[0] for row in cursor.fetchall()]
				if not cartriges:
					print ("Нет картриджей в наличии!")
					break
				cartrige=select(cartriges+['На уровень вверх',],'Выберите номер картриджа [0]:')
				if cartrige=='На уровень вверх': break
				print ("Списать картридж {0}?".format(cartrige))
				ans=what_to_do(('да','нет'))
				if ans=='д':
					QUERY = "UPDATE `assets` SET `StatusCode`=5 WHERE `AssetNumber`="+str(cartrige)
					cursor.execute(QUERY)
					print (QUERY)
					QUERY = "INSERT INTO `printer_cartridge`(`Printer`, `Cartridge`, `put`) VALUES ("+",".join((str(192),str(cartrige),"'"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))))+"')"
					cursor.execute(QUERY)
					print (QUERY)
					break
				elif ans=='н':
					print ('Отмена задачи')
					break
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
				if ans=='д':
					# поставить дату списания предыдущего картриджа
					QUERY="UPDATE `assets` SET `CancellationDate`='"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))+"' WHERE `AssetNumber`=(SELECT `pc`.`Cartridge` FROM `printer_cartridge` `pc` INNER JOIN `assets` `a` ON `pc`.`Cartridge`=`a`.`AssetNumber` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`Model`=`a`.`Model` WHERE `pc`.`Printer`="+str(printer[0])+" AND `pc`.`put`=(SELECT MAX(`put`) FROM `printer_cartridge` WHERE `Printer`="+str(printer[0])+" GROUP BY `Printer`) AND `cct`.`CartridgeType`= (SELECT `cct`.`CartridgeType` FROM `assets` `a` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`Model`=`a`.`Model` WHERE `a`.`AssetNumber`="+str(cartrige)+"))"
					cursor.execute(QUERY)
					print (QUERY)
					# списываем картридж, который устанавливаем
					QUERY = "UPDATE `assets` SET `StatusCode`=5 WHERE `AssetNumber`="+str(cartrige)
					cursor.execute(QUERY)
					print (QUERY)
					# вносим данные в таблицу картридж-принтер
					QUERY = "INSERT INTO `printer_cartridge`(`Printer`, `Cartridge`, `put`) VALUES ("+",".join((str(printer[0]),str(cartrige),"'"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))))+"')"
					cursor.execute(QUERY)
					print (QUERY)
				elif ans=='н':
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
def get_integer(message,default=0,min=0,max=100,allow_zero=True):
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
		if default=='None': default=''
	except ValueError:
		print("Значение по умолчанию должно быть строкой! Значение по умолчанию установлено в ''")
		default=''
	while True:
		result=input((message+":" if default=='' else message+" ["+default+"]:"))
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
def select(tuple,msg,selfname=False):
	""" Для обработки массивов из только из значений """
	for k,v in enumerate(tuple):
		print ("{0:<{2}}.{1}".format(k,v,get_shirina_nomera(tuple)))
	dop_ans=set(str(k) for k in range(len(tuple)))
	while True:
		ans=input(msg)
		if ans=='':
			return tuple[0]
		elif ans not in dop_ans:
			if not selfname:
				print("Ошибка! Допустимые варианты ответа:", str(",".join(sorted(dop_ans,key=int))))
			if selfname: return ans
		else:
			return tuple[int(ans)]
def select_with_name(tuple,msg,count,selfname=False):
	""" Для обработки массивов из пар значений """
	for k,v in enumerate(tuple):
		print ("{0:<{2}}.{1:<{4}}...<{3}>".format(k,v[1],get_shirina_nomera(tuple),v[0],get_shirina_stolbza([j[1] for j in tuple])))
	dop_ans=set(str(k) for k in range(len(tuple)))
	while True:
		ans=input(msg)
		if count==1:
			if ans=='':
				return tuple[0][0]
			if (ans not in dop_ans):
				if not selfname:
					print("Ошибка! Допустимые варианты ответа:", str(",".join(sorted(dop_ans,key=int))))
					continue
				if selfname: return ans
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
def get_float(message,default=None,min=0,max=100,allow_zero=True):
	try:
		default=float(default)
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
				if not min<=float(result)<=max:
					print ("Число должно быть не меньше {0} и не больше {1}".format(min,max))
				else:
					return float(result)
		except ValueError:
			print("Вводимое значение по умолчанию должно быть числом")

main()