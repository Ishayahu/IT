<?
include 'connection.php';

if (isset($_COOKIE['token'])):
	$token=$_COOKIE['token'];
	$r=mysql_query("SELECT `start`, `end` FROM `tokens` WHERE `token`='$token';");
	$f=mysql_fetch_array($r);
	$now=time();
	$arr1 = explode(" ", $f[start]);
	$arr2 = explode(" ", $f[end]);  
	$arrdate1 = explode("-", $arr1[0]);
	$arrdate2 = explode("-", $arr2[0]);
	$arrtime1 = explode(":", $arr1[1]);
	$arrtime2 = explode(":", $arr2[1]);
	$start = (mktime($arrtime1[0], $arrtime1[1], $arrtime1[2], $arrdate1[1],  $arrdate1[2],  $arrdate1[0]));
	$end = (mktime($arrtime2[0], $arrtime2[1], $arrtime2[2], $arrdate2[1],  $arrdate2[2],  $arrdate2[0]));
	if (($now - $start)<0):
		echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=2\"></HEAD><BODY></BODY></HTML>";
	//	echo "(now - start)<0";
	endif;
	if (($end - $now)<0):
		//echo "(end - now)<0";
		echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=3\"></HEAD><BODY></BODY></HTML>";
	endif;
	if (($end - $now)>0 and ($now - $start)>0):
		$r=mysql_query("UPDATE `tokens` SET `end`=DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 15 MINUTE) WHERE `token`='$token';");
		echo "<html>\n<head>\n<title>MySQL IT DB - Принтер-отдел</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
		mysql_connect("46.254.16.220","it","planrabot");
		mysql_query("set names utf8");
		mysql_select_db("it");
		//выбор категории активов
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
		echo "</table>\n</body></html>";
	endif;
else:
	echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=1\"></HEAD><BODY></BODY></HTML>";
endif;
?>