import sys, os,mysql.connector,time,datetime

LOGFILE_NAME='C:\IT\it.log'

def main():
	print ("Запуск скрипта")
	config={'use_unicode': True,
		'database': 'it',
		'charset': 'utf8',
		'host': '',
		'get_warnings': True,
		'user': '',
		'password': '',
		'port': 3306}
	config['host']=input('host: ')
	config['user']=input('user: ')
	config['password']=input('password: ')
	print (config)
	print ("Соединение с базой")
	db = mysql.connector.Connect(**config)
	print ("Получение курсора")
	cursor = db.cursor()
	while True:
		ans=what_to_do_stolb(('1.Замена картриджа и списание','2.Новый актив','3.Заказ картриджей','4.Инвентаризация картриджей','5.Работа со счетами','6-.Работа с заявками', '7.Отчет по бюджету','8.Ввод ремонта','В.Выход'))
		if ans=='1':
			cartrige_change(cursor)
		elif ans=='2':
			new_active(cursor)
		elif ans=='3':
			what_2_by(cursor)
		elif ans=='4':
			invent_cartridge(cursor)
		elif ans=='5':
			bills_cashless(cursor)
		elif ans=='6':
			new_zayavka(cursor)
		elif ans=='7':
			budjet(cursor)
		elif ans=='8':
			repairing(cursor)

		elif ans=='в': exit()
		ans=what_to_do(('Продолжить','Выйти'))
		if ans=='в': exit()
def new_zayavka(cursor):
	pass
def bill_delete(cursor,ID):
	# составление списка запросов: удаление активов и счёта
	# выбираем все активы, привязанные к этому счёту и удаляем их
	QUERY1='DELETE FROM `assets` WHERE `BillCashlessNumber`='+ID+";"
	# удаляем счёт
	QUERY2='DELETE FROM `billcashless` WHERE `ID`='+ID+";"
	queries=(QUERY1,QUERY2)
	query_logging(cursor,*queries,name='Удаление счёта'+ID)
def bill_close(cursor,ID):
	logging('Закрытие счёта'+ID)
	year, month, day, hour, minutes, sec=get_datatime()
	# выбираем все активы, привязанные к этому счёту и меняем им статус, серийный номер, гарантия, номер гарантии, дату покупки
	# меняем статус и дату покупки и номер гарантии так как это у всех одинаково
	GarantyNumber=get_integer('Введите номер гарантии',default=0,min=0,max=999,allow_zero=True)
	QUERY=["UPDATE `assets` SET `ByeDate`='"+"-".join((str(year),str(month),str(day)))+"',`GarantyNumber`="+str(GarantyNumber)+",`StatusCode`=0 WHERE `BillCashlessNumber`="+ID+";"]
							#logging(QUERY)
							#cursor.execute(QUERY)
	# проход по активам по одному
	QUERY_TMP="SELECT `AssetNumber`,`Model` FROM `assets` WHERE `BillCashlessNumber`="+ID+";"
	cursor.execute(QUERY_TMP)
	assets=[]
	models=[]
	for k,k1 in [(str(row[0]),row[1]) for row in cursor.fetchall()]:
		assets.append(k)
		models.append(k1)
	#assets=(282,283)
	for k in range(len(assets)):
		# серийный номер, гарантия
		SerialNumber=get_string('Введите серийный номер актива '+models[k]+' №'+str(assets[k]),default='',min=0,max=100,allow_zero=True)
		Garanty=get_integer('Введите срок гарантии актива '+models[k]+' №'+str(assets[k]),default=0,min=0,max=999,allow_zero=True)
		QUERY+=["UPDATE `assets` SET `SerialNumber`="+str(SerialNumber)+" `Garanty`="+str(Garanty)+" WHERE `AssetNumber` ="+str(assets[k])+";"]
							#logging(QUERY)
							#cursor.execute(QUERY)
	# закрываем счёт
	QUERY+=["UPDATE `billcashless` SET `Peselev`=1,`Motya`=1,`Boroda`=1,`Oplata`=1,`Documents`=1,`DocReturnDate`='"+"-".join((str(year),str(month),str(day)))+"',`DeliveryDate`='"+"-".join((str(year),str(month),str(day)))+"' WHERE `ID`="+ID+";"]
							#logging(QUERY)	
							#cursor.execute(QUERY)
	query_logging(cursor,*QUERY,name='Закрытие счёта №'+ID)
def bills_cashless(cursor):
	stages=("ИЯ","Мотя","Борода","Оплата","Документы")
	SELECT_WHAT_IS="SELECT `ID`, `BilNumber`, `DistributorName`, `Peselev`, `Motya`, `Boroda`, `Oplata`, `Documents`, `DocReturnDate`, `DeliveryDate` FROM `billcashless` WHERE `Documents` =0 OR `Peselev` =0 OR `Motya` =0 OR `Boroda` =0;"
	while True:
		cursor.execute(SELECT_WHAT_IS)
		bills=[row for row in cursor.fetchall()]
		show_bills(["{0} от {1}".format(x[1],x[2] )for x in bills],[(x[3],x[4],x[5],x[6],x[7]) for x in bills])
		print ("{0}.Новый счёт".format(len(bills)))
		print ("{0}.На уровень вверх".format(len(bills)+1))
		
		#print ([(k,v[1]) for k,v in enumerate(bills)])
		bill=select_with_name([(k,v[1]) for k,v in enumerate(bills)]+[('Н','Новый счёт'),('В','На уровень вверх')],'Выберите номер счета [0]:',2,verbouse=False)
		if bill[0]=='В': break
		print (bill[0])
		if bill[0]=='Н':
			new_bill(cursor)
			continue
			# возврат (номер порядковый из таблицы, номер счета) - использовать номер ID, определяемый по внутреннему порядковуму номеру
			# обработка выбранного счёта
			
			# проверить корректность данных
		flag=bills[bill[0]][3]
		for k in range(3,8):
			if not flag and bills[bill[0]][k]:# ...0,1...
				print ('Нужна корректировка данных счёта!')
			flag=1 if bills[bill[0]][k] else 0
			# изменить что надо
		changed=False
		last_stage=get_integer('Введите номер последнего этапа (-1-удалить, 5-закрыть):',default=1,min=-1,max=len(stages),allow_zero=False)
		# удаление счёта если laststage='0'
		if last_stage==-1:
			ans=what_to_do(('Удалить?','Отмена!'))
			if ans=='о': continue
			bill_delete(cursor,str(bills[bill[0]][0]))
			continue
		# закрытие счёта если laststage='5'
		if last_stage==5:
			ans=what_to_do(('Закрыть?','Отмена!'))
			if ans=='о': continue
			bill_close(cursor,str(bills[bill[0]][0]))
			continue

		tmp=[]
		for k in range(0,len(stages)):
			x=1 if k<last_stage else 0
			tmp.append(x)
			# есть ли изменения? записать
		changed=False if tmp==list(bills[bill[0]][3:8]) else True
		if changed:
			UPDATE_Q="UPDATE `billcashless` SET  `Peselev`="+str(tmp[0])+",`Motya`="+str(tmp[1])+",`Boroda`="+str(tmp[2])+",`Oplata`="+str(tmp[3])+",`Documents`="+str(tmp[4])+" WHERE `ID`="+str(bills[bill[0]][0])
			query_logging(cursor,UPDATE_Q,name='Изменение состояния счёта '+str(bills[bill[0]][0]))
def get_datatime():
	now = datetime.datetime.now() 
	year, month, day, hour, minutes, sec, wday, yday, isdst = now.timetuple()  
	if month<10: month = "0%s" % month
	if day<10: day = "0%s" % day
	return year, month, day, hour, minutes, sec
def get_distributor(cursor):
	QUERY="SELECT `d`.`DistributorName` FROM `distributors` `d` LEFT OUTER JOIN `assets` `a` ON `a`.`DistributorName`=`d`.`DistributorName` GROUP BY `d`.`DistributorName` ORDER BY COUNT(`a`.`DistributorName`) DESC"
	cursor.execute(QUERY)
	distributers=[row[0] for row in cursor.fetchall()]
	DistributorName=select(distributers,'Выберите поставщика [0]: ')
	return str(DistributorName)
def logging(*strings):
	logfile=open(LOGFILE_NAME,'a')
	year, month, day, hour, minutes, sec=get_datatime()
	logfile.write("-".join((str(year),str(month),str(day)))+' '+":".join((str(hour),str(minutes),str(sec)))+'\n')
	for string in strings:
		logfile.write(string+'\n')
	logfile.close()
def query_logging(cursor,*queries,name=''):
	"""Функция для ведения лога запросов"""
	#print (queries)
	#exit()
	logfile=open(LOGFILE_NAME,'a')
	year, month, day, hour, minutes, sec=get_datatime()
	logfile.write(name+"-".join((str(year),str(month),str(day)))+' '+":".join((str(hour),str(minutes),str(sec)))+'\n')
	for query in queries:
		logfile.write(query[0] if type(query)==list else query)
		cursor.execute(query[0] if type(query)==list else query)
		logfile.write('...OK\n')
	logfile.close()
def new_bill(cursor):
	year, month, day, hour, minutes, sec=get_datatime()
	BilNumber=get_string('Введите номер счёта',default='+++',min=1,max=100,allow_zero=False)
	DistributorName=get_distributor(cursor)
	# получить ID этого счёта в таблице
	QUERY_ID="SELECT MAX(`ID`) FROM `billcashless`;"
	cursor.execute(QUERY_ID)
	ID=[row[0] for row in cursor.fetchall()][0]+1
	#log=''
	QUERY_U=[]
	while True:
		QUERY_U+=new_active(cursor,status=6,BillCashlessNumber=ID,BillNumber=BilNumber,DistributorName=DistributorName)
		ans=what_to_do(('Ввести еще актив','Продолжить'))
		if ans=='п': break
	# записать счет в таблицу
	QUERY_U+=["INSERT INTO `billcashless`(`ID`, `BilNumber`, `DistributorName`,`BillDate`, `Peselev`, `Motya`, `Boroda`, `Oplata`, `Documents`, `DocReturnDate`, `DeliveryDate`) VALUES ("+str(ID)+",'"+str(BilNumber)+"','"+str(DistributorName)+"','"+"-".join((str(year),str(month),str(day)))+"',0,0,0,0,0,'0000-00-00','0000-00-00')"]
	# запись в логи
	#logging(log,QUERY_U)
	query_logging(cursor,QUERY_U,name='Ввод счёта №'+str(ID)+' после ввода активов')
								#cursor.execute(QUERY_U)
	#print (QUERY_U)
	# получение купленых товаров для сопроводиловки
	QUERY='SELECT CONCAT(`ac`.`Name`,", модель ",`a`.`Model`) FROM `assets` `a` INNER JOIN `assetcategory` `ac` ON `ac`.`AssetCategoryNumber`=`a`.`AssetCategoryNumber` WHERE `a`.`BillCashlessNumber`='+str(ID)+";"
	cursor.execute(QUERY)
	what_in_bill=''
	for k in [row[0] for row in cursor.fetchall()]:
		what_in_bill=what_in_bill+k+"; "
	what_in_bill=what_in_bill[:-2]
	# получение суммы счёта
	QUERY='SELECT SUM(`a`.`Price`) FROM `assets` `a` WHERE `a`.`BillCashlessNumber`='+str(ID)+" GROUP BY `a`.`BillCashlessNumber`;"
	cursor.execute(QUERY)
	bill_price=[row[0] for row in cursor.fetchall()][0]
	sopr='В приемную господина Вайсберга\nПрошу Вас разрешить оплату счёта '+str(BilNumber)+' от '+"-".join((str(year),str(month),str(day)))+'\nНа сумму '+str(bill_price)+' руб.\nЦелевое назначение: '+what_in_bill+'\nОбъект  - Склад\nСвоевременное предоставление документов гарантирую.\nОтветственное лицо: Ластов Ишаяу\nКонтактные телефоны: +7-901-569-81-86; 645-05-16\nДата '+"-".join((str(year),str(month),str(day)))+'\nРасписка в приеме документов по произведенной оплате:\nОригинал счёта\nДоговор\nАкт\nНакладная\nСчёт-фактура'
	temp=open('it.txt','w')
	temp.write(sopr)
	temp.close()
	os.startfile('it.txt')
def show_bills(list,datas):
	"""функция для отображения полученных счетов с их данными в таблице (список счетов, список данных:("ИЯ","Мотя","Борода","Оплата","Документы"), 0-нет, 1-да)"""
	# этапы прохождения счёта
	stages=("ИЯ","Мотя","Борода","Оплата","Документы")
	# если список счетов пустой
	if not list:
		print ("Нет счётов")
		return
	# получение количества строк со счетами в таблице
	rows=len(list)
	# получение количества столбцов для этапов счетов
	columns=len(stages)
	# ширина столбца со счетами
	width=int(get_shirina_stolbza(list)) if int(get_shirina_stolbza(list))>len("№ счета") else len("№ счета")
	# вычисление полной ширины таблицы
	width_full=width
	# вычисление ширины столбца с порядковым номером счета
	width_number=get_shirina_nomera(list)
	# добавляем к общей ширине ширину каждого столбца
	for k in stages:
		width_full+=int(len(k))
	# выводим шапку
	# ("+{1}+{0}+".format("-"*ширина счетов,"-"*ширина номера счета)+"+".join(("-"*z for z in (int(len(j)) for j in stages)))+"+")
	# по поводу "+".join(("-"*z for z in (int(len(j)) for j in stages)))+"+")
	# (int(len(j)) for j in stages) - список содержащий длины столбцов этапов
	# ("-"*z for z in (список)) - список из строк "-" длиной в ширину соответствующего столбца
	print ("+{1}+{0}+".format("-"*width,"-"*width_number)+"+".join(("-"*z for z in (int(len(j)) for j in stages)))+"+")
	print ("+{0:^{3}}+{1:^{2}}".format("№","№ счета",width,width_number)+"+"+"+".join((stages))+"+")
	print ("+{1}+{0}+".format("-"*width,"-"*width_number)+"+".join(("-"*z for z in (int(len(j)) for j in stages)))+"+")
	# выводим сами счета
	for k in range(rows):
		tmp=''
		for j in range(columns):
		# формируем строку с отметками о проходе
			tmp+="{0:^{1}}|".format("*" if datas[k][j] else " ",len(stages[j]))
		print ("|{2:<{3}}|{0:<{1}}".format(list[k],width,k,width_number)+"|"+tmp)
		print ("+{1}+{0}+".format("-"*width,"-"*width_number)+"+".join(("-"*z for z in (int(len(j)) for j in stages)))+"+")
def get_payment_metod():
	MethodOfPayment=what_to_do_stolb(('Cash','NonCash')).upper()
	if MethodOfPayment=='N': MethodOfPayment='NC'
	return MethodOfPayment
def repairing(cursor):
	AssetNumber=get_integer('Введите номер актива для ремонта',max=0)
	QUERY_ID="SELECT `a`.`Model`, `ac`.`Name` FROM `assets` `a` INNER JOIN `assetcategory` `ac` ON `ac`.`AssetCategoryNumber`=`a`.`AssetCategoryNumber` WHERE `a`.`AssetNumber`="+str(AssetNumber)+";"
	cursor.execute(QUERY_ID)
	Model,Cat=[row for row in cursor.fetchall()][0]
	print ("Вы выбрали ремонт {0} модели {1} номер {2}".format(Cat,Model,AssetNumber))
	ans=what_to_do(('Продолжить','Отмена'))
	if ans=='о': return
	Breakdown=get_string("Введите описание поломки",allow_zero=False)
	DistributorName=get_distributor(cursor)
	StartDate=get_string("Введите дату начала ремонта в формате YYYY-MM-DD",allow_zero=False)
	EndDate=get_string("Введите дату конца ремонта в формате YYYY-MM-DD",allow_zero=False)
	Garanty=get_integer('Введите срок гарантии',min=0,max=999,allow_zero=True)
	Price=get_integer('Введите цену ремонту',default=0,min=0,max=0,allow_zero=True)
	BillDate=get_string("Введите дату счёта YYYY-MM-DD",allow_zero=False)
	GarantyNumber=get_integer('Введите номер гарантии',min=0,max=0,allow_zero=True)
	BillNumber=get_string("Введите номер счёта",allow_zero=False)
	MethodOfPayment=get_payment_metod()
	QUERY_U='INSERT INTO `repairing`(`ID`, `AssetNumber`, `Breakdown`, `DistributorName`, `StartDate`, `EndDate`, `Garanty`, `Price`, `BillDate`, `GarantyNumber`, `BillNumber`, `MethodOfPayment`) VALUES (null,'+",".join((str(AssetNumber), "'"+Breakdown+"'", "'"+DistributorName+"'", "'"+StartDate+"'", "'"+EndDate+"'", str(Garanty), str(Price),  "'"+BillDate+"'", str(GarantyNumber),  "'"+BillNumber+"'",  "'"+MethodOfPayment+"'"))+");"
	logging (QUERY_U)
	cursor.execute(QUERY_U)
def invent_cartridge(cursor):
	SELECT_WHAT_IS="SELECT `Model`,`AssetNumber` FROM `assets` WHERE `AssetCategoryNumber`=1 AND `StatusCode`=0 ORDER BY `Model`;"
	cursor.execute(SELECT_WHAT_IS)
	what_is=[row for row in cursor.fetchall()]
	file=open('invent.txt','w',encoding='utf8')
	for k in what_is:
		file.write("{0:.<{2}}...<{1}>".format(k[0],k[1],get_shirina_stolbza([z[0] for z in what_is]))+'\n')
	file.close()
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
		file.write('"Дата","Расход","Остаток","На что","Чек","Категория"\n')
		summ=25000
		for k in TMP:
			summ=summ-int(k[1])
			file.write(','.join((str(k[0]),str(k[1]),str(summ),str(k[2]),'"'+str(k[3])+'"',acat[k[4]]))+'\n')
		QUERY = "SELECT `BillDate`, `Price`, `Breakdown`, `BillNumber` FROM `repairing` WHERE `BillDate` < '"+str(year)+"-"+str(month+1)+"-01' AND `BillDate` >= '"+str(year)+"-"+str(month)+"-01' AND `MethodOfPayment`='"+MethodOfPayment+"' ORDER BY `BillDate` ASC"
		cursor.execute(QUERY)
		TMP=[row for row in cursor.fetchall()]
		for k in TMP:
			summ=summ-int(k[1])
			file.write(','.join((str(k[0]),str(k[1]),str(summ),str(k[2]),'"'+str(k[3])+'"','Ремонт'))+'\n')
		file.close()
def new_active(cursor,status=0,BillCashlessNumber=-1,BillNumber='',DistributorName=''):
	""" Ввод нового актива, status=0 для новго просто, 6 - для нового, введенного в заказ; BillCashlessNumber=-1 для купленного не по счёту, иначе - номер счёта из таблицы 
	при безнал возвращает запрос для выполнения его вместе с формированием счёта
	"""
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
				#SerialNumber=get_string('Введите серийный номер актива',default='',min=0,max=100,allow_zero=True)
				if not status==6:
					StatusCode=select_with_name([(0,'Новое'),(1,'Б/У'),(2,'Глючное'),(3,'Не рабочее'),(4,'Возврат по гарантии'),(5,'Списано')],'Выберите статус актива [0]:',2)
				else:
					StatusCode=6
				Garanty=get_integer('Введите срок гарантии',default=0,min=0,max=999,allow_zero=True)
				if not BillNumber:
					BillNumber=get_string('Введите номер чека',default='',min=0,max=100,allow_zero=False)
				if not DistributorName:
					#QUERY="SELECT `d`.`DistributorName` FROM `distributors` `d` LEFT OUTER JOIN `assets` `a` ON `a`.`DistributorName`=`d`.`DistributorName` GROUP BY `d`.`DistributorName` ORDER BY COUNT(`a`.`DistributorName`) DESC"
					#cursor.execute(QUERY)
					#distributers=[row[0] for row in cursor.fetchall()]
					#DistributorName=select(distributers,'Выберите поставщика [0]: ')
					DistributorName=get_distributor(cursor)
				Price=get_float('Введите цену актива',default=0,min=0,max=25000,allow_zero=True)
				#print (BillCashlessNumber)
				#print (BillCashlessNumber!=-1)
				if BillCashlessNumber==-1:
					MethodOfPayment=what_to_do_stolb(('Cash','NonCash')).upper()
					if MethodOfPayment=='N': MethodOfPayment='NC'
				GarantyNumber=get_integer('Введите номер гарантии',default=0,min=0,max=999,allow_zero=True) if Garanty else 0
				copies=get_integer('Введите количество экземпляров',default=1,min=1,max=100,allow_zero=False)
				QUERY=[]
				for copie in range(1,copies+1):
					SerialNumber=get_string('Введите серийный номер актива',default='',min=0,max=100,allow_zero=True)
					# если оплата за наличный расчёт
					if BillCashlessNumber==-1:
						QUERY+=["INSERT INTO `assets`(`AssetNumber`, `AssetCategoryNumber`, `Model`, `SerialNumber`, `StatusCode`, `Place`, `PCName`, `ByeDate`, `Garanty`, `Notes`, `Price`, `DistributorName`, `BillNumber`, `MethodOfPayment`, `GarantyNumber`, `CancellationDate`) VALUES ("+",".join(('null',str(category[0]),"'"+model+"'",("'"+SerialNumber+"'" if SerialNumber else "''"),str(StatusCode[0]), "'Склад'", 'null', "'"+"-".join((str(year),str(month),str(day)))+"'", str(Garanty), 'null', str(Price), "'"+DistributorName+"'", "'"+BillNumber+"'", "'"+MethodOfPayment+"'", str(GarantyNumber), "'0000-00-00'"))+")"]
					# если оплата по безналу
					else:
						QUERY+=["INSERT INTO `assets`(`AssetNumber`, `AssetCategoryNumber`, `Model`, `SerialNumber`, `StatusCode`, `Place`, `PCName`, `ByeDate`, `Garanty`, `Notes`, `Price`, `DistributorName`, `BillNumber`,  `BillCashlessNumber`,`MethodOfPayment`, `GarantyNumber`, `CancellationDate`) VALUES ("+",".join(('null',str(category[0]),"'"+model+"'",("'"+SerialNumber+"'" if SerialNumber else "''"),"'"+str(StatusCode)+"'", "'Склад'", 'null', "'"+"-".join((str(year),str(month),str(day)))+"'", str(Garanty), 'null', str(Price), "'"+DistributorName+"'", "'"+str(BillNumber)+"'", "'"+str(BillCashlessNumber)+"'", "'NC'", str(GarantyNumber), "'0000-00-00'"))+")"]
						return QUERY
				#print (QUERY)
				#logging(QUERY)
				#cursor.execute(QUERY)
				query_logging(cursor,*QUERY,name='Ввод активов:')
				# вернуть введенный номер
				QUERY2="SELECT MAX(`AssetNumber`) FROM `assets`"
				cursor.execute(QUERY2)
				number=[row[0] for row in cursor.fetchall()][0]
				if copies==1:
					print ("Номер актива: ",number)
				else:
					print ("Номера активов с {0} по {1}".format(number-copies+1, number))
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
		logging('Списание картриджа')
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
					logging (QUERY)
					QUERY = "INSERT INTO `printer_cartridge`(`Printer`, `Cartridge`, `put`) VALUES ("+",".join((str(192),str(cartrige),"'"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))))+"')"
					cursor.execute(QUERY)
					logging (QUERY)
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
					logging('Замена картриджа')
					# поставить дату списания предыдущего картриджа
					Q1="SELECT `pc`.`Cartridge` tmp1 FROM `printer_cartridge` `pc` INNER JOIN `assets` AS `a` ON `pc`.`Cartridge`=`a`.`AssetNumber` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`Model`=`a`.`Model` WHERE `pc`.`Printer`="+str(printer[0])+" AND `pc`.`put`=(SELECT MAX(`pc`.`put`) FROM `printer_cartridge` `pc` INNER JOIN `assets` AS `a` ON `pc`.`Cartridge`=`a`.`AssetNumber` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`Model`=`a`.`Model` WHERE `pc`.`Printer`="+str(printer[0])+" AND `cct`.`CartridgeType`=(SELECT `cct`.`CartridgeType` FROM `assets` AS `a` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`Model`=`a`.`Model` WHERE `a`.`AssetNumber`="+str(cartrige)+"))  AND `cct`.`CartridgeType`=(SELECT `cct`.`CartridgeType` FROM `assets` AS `a` INNER JOIN `cartridge_cartridge_type` `cct` ON `cct`.`Model`=`a`.`Model` WHERE `a`.`AssetNumber`="+str(cartrige)+")"
					cursor.execute(Q1)
					for k in cursor.fetchall():
						assetnumber=k[0]
					if "assetnumber" in locals():
						print (assetnumber)
						QUERY="UPDATE `assets` SET `CancellationDate`='"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))+"' WHERE `AssetNumber`="+str(assetnumber)
						logging (QUERY)
						cursor.execute(QUERY)
					
					# списываем картридж, который устанавливаем
					QUERY = "UPDATE `assets` SET `StatusCode`=5 WHERE `AssetNumber`="+str(cartrige)
					logging (QUERY)
					cursor.execute(QUERY)
					
					# вносим данные в таблицу картридж-принтер
					QUERY = "INSERT INTO `printer_cartridge`(`Printer`, `Cartridge`, `put`) VALUES ("+",".join((str(printer[0]),str(cartrige),"'"+"-".join((str(year),str(month),str(day)))+" "+":".join((str(hour),str(minutes),str(sec)))))+"')"
					logging (QUERY)
					cursor.execute(QUERY)
					
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
	"""max=0 - нет ограничения по максимуму"""
	try:
		default=int(default)
	except ValueError:
		print("Значение по умолчанию должно быть числом! Значение по умолчанию установлено в 0")
		default=0
	while True:
		try:
			#print (default)
			result=input((message+":" if not default else message+" ["+str(default)+"]:"))
			if not result:
				if default:
					return default
				if allow_zero:
					return 0
			else:
				if max!=0:
					if not min<=int(result)<=max:
						print ("Число должно быть не меньше {0} и не больше {1}".format(min,max))
					else:
						return int(result)
				else:
					if not min<=int(result):
						print ("Число должно быть не меньше {0}".format(min))
					else:
						return int(result)
		except ValueError:
			print("Вводимое значение по умолчанию должно быть числом")
def get_string(message,default=None,min=0,max=100,allow_zero=True):
	"""max=0 - нет ограничения по максимуму"""
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
				return str(defaul)
			if allow_zero:
				return ''
		else:
			if max!=0:
				if not min<len(result)<max:
					print ("Длина строки должна быть не меньше {0} и не больше {1}".format(min,max))
				else:
					return str(result)
			else:
				if not min<len(result):
					print ("Длина строки должна быть не меньше {0}".format(min))
				else:
					return str(result)
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
def select_with_name(tuple,msg,count,selfname=False,verbouse=True):
	""" Для обработки массивов из пар значений verbouse-выводить ли варианты выбора"""
	if verbouse:
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
	"""функция для получения данных как число с точкой (сообщение для вывода на экран,значение по умолчанию=0,минимальное значение=0,максимальное значение=100,разрешен ли ввод нуля=True)"""
	try:
		default=float(default)
	except ValueError:
		# если значение, переданное по умолчанию, не может быть переведено в число
		print("Значение по умолчанию должно быть числом! Значение по умолчанию установлено в 0")
		default=0
	while True:
		try:
			result=input((message+":" if not default else message+" ["+str(default)+"]:"))
			# если ничего не введено
			if not result:
				# если есть значение по умолчанию
				if default:
					return default
				# если запрашиваемое значение может быть равно нулю - пустой ввод это и значит
				if allow_zero:
					return 0
				# если значение не введено и не может быть нулем - запускаем цикл заново
			# если что-то введено
			else:
				# если находится вне заданного 
				if not min<=float(result)<=max:
					print ("Число должно быть не меньше {0} и не больше {1}".format(min,max))
				else:
				# возвращаем введенное значение
					return float(result)
		except ValueError:
			# если значение не может быть переведено в число
			print("Вводимое значение по умолчанию должно быть числом")

main()