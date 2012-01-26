<?
echo "<html>\n<head>\n<title>MySQL IT DB - Принтер-отдел</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
		//редактирование записей
		if (isset($_GET['edit'])):
		$edit=mysql_escape_string($_GET['edit']);
		else:
		$edit=-1;
		endif;

		if (isset($_GET['save']) and $_GET['save']=="Сохранить"):
			$department=mysql_escape_string($_GET['department']);
			$ID=mysql_escape_string($_GET['ID']);
			$printer=mysql_escape_string($_GET['printer']);
			$puted=mysql_escape_string($_GET['puted']);
			$removed=mysql_escape_string($_GET['removed']);
			$r=mysql_query("UPDATE `printer_department` SET `Printer`=$printer,`Department`='$department',`puted`='$puted',`removed`='$removed' WHERE `ID`= $ID;");
			echo "Done: UPDATE `printer_department` SET `Printer`=$printer,`Department`='$department',`puted`='$puted',`removed`='$removed' WHERE `ID`= $ID;\nResilt: $r";
		endif;
		if (isset($_GET['saveNew']) and $_GET['saveNew']=="Добвить"):
			$DepartmentNew=mysql_escape_string($_GET['DepartmentNew']);
			$PrinterNew=mysql_escape_string($_GET['PrinterNew']);
			$putedNew=mysql_escape_string($_GET['putedNew']);
			$r=mysql_query("INSERT INTO `printer_department`(`ID`, `Printer`, `Department`, `puted`, `removed`) VALUES (null,'$PrinterNew','$DepartmentNew','$putedNew','0000-00-00 00:00:00');");
			echo "Done: INSERT INTO `printer_department`(`ID`, `Printer`, `Department`, `puted`, `removed`) VALUES (null,'$PrinterNew','$DepartmentNew','$putedNew','0000-00-00 00:00:00');\nResilt: $r";
		endif;

		/*department=012
		printer=189
		puted=2011-09-25+00%3A00%3A00
		removed=0000-00-00+00%3A00%3A00
		save=%D0%A1%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D1%82%D1%8C*/

		echo "<table border=1 width=100%>\n";
		echo "<tr><td>№</td><td>Отдел</td><td>Принтер</td><td>Поставлен</td><td>Редактирование</td></tr>\n";
		$r=mysql_query("SELECT `pd`.`ID`, `a`.`Model`, `pd`.`Department`, `pd`.`puted`, `pd`.`removed` FROM `printer_department` `pd` INNER JOIN `assets` `a` ON `pd`.`Printer`=`a`.`AssetNumber` WHERE `pd`.`removed`='0000-00-00 00:00:00';");
		for ($i=0; $i<mysql_num_rows($r);$i++)
		{
		if ($i%2==0):
			echo "<tr bgcolor=\"grey\">";
		else:
			echo "<tr bgcolor=\"white\">";
		endif;
		$f=mysql_fetch_array($r);

		if ($f[ID]==$edit):
			echo "<form action=\"it-printer_department.php\" method=\"GET\">\n";
			echo "<td>$f[ID]<input type=\"hidden\" name=\"ID\" value=\"$f[ID]\"></td>";
			$departments=mysql_query("SELECT `Department` FROM `departments`;");
				echo "<td><select name=\"department\" size=1>\n";
				for ($x=0; $x<mysql_num_rows($departments);$x++)
				{
				$y=mysql_fetch_array($departments);
				echo "<option value=$y[Department]>$y[Department]</option>\n";
				}
				echo "</select></td>\n";
			$printers=mysql_query("(SELECT `a`.`Model`,`a`.`AssetNumber` FROM `assets` `a` LEFT OUTER JOIN `printer_department` `pd` ON `a`.`AssetNumber`=`pd`.`Printer` WHERE `a`.`AssetCategoryNumber`='0' AND `pd`.`Department` IS NULL AND `a`.`StatusCode`<>5) UNION ALL (SELECT DISTINCT `a`.`Model`,`a`.`AssetNumber` FROM `printer_department` `pd` INNER JOIN `assets` `a` ON `pd`.`Printer`=`a`.`AssetNumber` WHERE `a`.`StatusCode`<>5 AND 0=ALL (SELECT CASE WHEN `pd1`.`removed`<>'0000-00-00 00:00:00' AND `pd1`.`puted`<>'0000-00-00 00:00:00' THEN 0 ELSE 1 END FROM `printer_department` `pd1` WHERE `pd`.`Printer`=`pd1`.`Printer`));");
			/*(SELECT `a`.`Model`,`a`.`AssetNumber`,`pd`.`Department`,`pd`.`puted`,`pd`.`removed` FROM `assets` `a` LEFT OUTER JOIN `printer_department` `pd` ON `a`.`AssetNumber`=`pd`.`Printer` WHERE `a`.`AssetCategoryNumber`='0' AND `pd`.`Department` IS NULL AND `a`.`StatusCode`<>5)
		UNION ALL
		(SELECT DISTINCT `a`.`Model`,`a`.`AssetNumber`,`pd`.`Department`,`pd`.`puted`,`pd`.`removed` FROM `printer_department` `pd` INNER JOIN `assets` `a` ON `pd`.`Printer`=`a`.`AssetNumber` WHERE `a`.`StatusCode`<>5 AND 0=ALL (SELECT
			CASE
				WHEN `pd1`.`removed`<>'0000-00-00 00:00:00' AND `pd1`.`puted`<>'0000-00-00 00:00:00' THEN 0
				ELSE 1
			END
		FROM `printer_department` `pd1` WHERE `pd`.`Printer`=`pd1`.`Printer`)
		);*/
				echo "<td><select name=\"printer\" size=1>\n";
				for ($x=0; $x<mysql_num_rows($printers);$x++)
				{
				$y=mysql_fetch_array($printers);
				echo "<option value=$y[AssetNumber]>$y[AssetNumber]...$y[Model]</option>\n";
				}
				echo "</select></td>\n";
			echo "<td><input type=\"text\" name=\"puted\" value=\"$f[puted]\"></td>";
			echo "<td><input type=\"text\" name=\"removed\" value=\"$f[removed]\"><input type=\"submit\" name=\"save\" value=\"Сохранить\"></td>";
		else:
			echo "<td>$f[ID]</td><td>$f[Department]</td><td>$f[Model]</td><td>$f[puted]</td><td><a href=\"it-printer_department.php?edit=$f[ID]\">Редактировать</a></td>";
		endif;

		echo "</tr>\n";
		}
		echo "</table>\n<br>";
		// ввод нового принтера
		echo "<form action=\"it-printer_department.php\" method=\"GET\">\n<b>Добавление новой записи</b><table><tr><td>\n";
			$printers=mysql_query("(SELECT `a`.`Model`,`a`.`AssetNumber` FROM `assets` `a` LEFT OUTER JOIN `printer_department` `pd` ON `a`.`AssetNumber`=`pd`.`Printer` WHERE `a`.`AssetCategoryNumber`='0' AND `pd`.`Department` IS NULL AND `a`.`StatusCode`<>5) UNION ALL (SELECT DISTINCT `a`.`Model`,`a`.`AssetNumber` FROM `printer_department` `pd` INNER JOIN `assets` `a` ON `pd`.`Printer`=`a`.`AssetNumber` WHERE `a`.`StatusCode`<>5 AND 0=ALL (SELECT CASE WHEN `pd1`.`removed`<>'0000-00-00 00:00:00' AND `pd1`.`puted`<>'0000-00-00 00:00:00' THEN 0 ELSE 1 END FROM `printer_department` `pd1` WHERE `pd`.`Printer`=`pd1`.`Printer`));");
				echo "<select name=\"PrinterNew\" size=1>\n";
				for ($x=0; $x<mysql_num_rows($printers);$x++)
				{
				$y=mysql_fetch_array($printers);
				echo "<option value=$y[AssetNumber]>$y[AssetNumber]...$y[Model]</option>\n";
				}
				echo "</select></td>\n";
			echo "<td>\n";
			$departments=mysql_query("SELECT `Department` FROM `departments`;");
				echo "<select name=\"DepartmentNew\" size=1>\n";
				for ($x=0; $x<mysql_num_rows($departments);$x++)
				{
				$y=mysql_fetch_array($departments);
				echo "<option value=$y[Department]>$y[Department]</option>\n";
				}
				echo "</select></td>\n";
			
			$nowNew=date("Y-m-d H:i:s");
			
			echo "<td><input type=\"text\" name=\"putedNew\" value=\"$nowNew\"></td>";
			echo "<td><input type=\"submit\" name=\"saveNew\" value=\"Добвить\"></td></tr></table>";

			echo "</body></html>";	

?>