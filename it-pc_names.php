<?
mysql_connect("","","");
mysql_query("set names utf8");
mysql_select_db("it");

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
		echo "<html>\n<head>\n<title>MySQL IT DB - Компьютеры</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
		mysql_connect("46.254.16.220","it","planrabot");
		mysql_query("set names utf8");
		mysql_select_db("it");
		// обработка удаления
		if (isset($_GET['delete'])):
			$delete=mysql_escape_string($_GET['delete']);
			$r=mysql_query("DELETE FROM `pcnames` WHERE `PCName`='$delete';");
			echo "Done: DELETE FROM `pcnames` WHERE `PCName`='$delete';\nResilt: $r";
		endif;
		// обработка редактирования
		if (isset($_GET['edit'])):
		$edit=mysql_escape_string($_GET['edit']);
		else:
		$edit=-1;
		endif;

		if (isset($_GET['save_edit']) and $_GET['save_edit']=="Сохранить"):
			$PCName=mysql_escape_string($_GET['PCName']);
			$Notes=mysql_escape_string($_GET['Notes']);
			$IP=mysql_escape_string($_GET['IP']);
			$r=mysql_query("UPDATE `pcnames` SET `Notes`='$Notes',`IP`='$IP' WHERE `PCName`='$PCName';");
			echo "Done: UPDATE `pcnames` SET `Notes`='$Notes',`IP`='$IP' WHERE `PCName`='$PCName';\nResilt: $r";
		endif;

		//если новая категория актива
		if (isset($_GET['new_pc']) and isset($_GET['save_new']) and $_GET['save_new']=="Сохранить"):
		$new_pc=mysql_escape_string($_GET['new_pc']);
		$notes=mysql_escape_string($_GET['notes']);
		$ip=mysql_escape_string($_GET['ip']);
		$r=mysql_query("INSERT INTO `pcnames`(`PCName`, `Notes`, `IP`) VALUES ('$new_pc','$notes','$ip');");
		echo "Done: INSERT INTO `pcnames`(`PCName`, `Notes`, `IP`) VALUES ('$new_pc','$notes','$ip');\nResilt: $r";
		endif;

		// ввод нового ПК
		echo "<form action=\"it-pc_names.php\" method=\"GET\">\n<table border=1 width=100%>\n<tr><td>Имя</td><td>Примечания</td><td>IP</td></tr>\n<tr><td><input type=\"text\" name=\"new_pc\" value=\"\"></td><td><input type=\"text\" name=\"notes\" value=\"\" size=60></td><td><input type=\"text\" name=\"ip\" value=\"\"></td></tr></table><br><input type=\"submit\" name=\"save_new\" value=\"Сохранить\"><br>";

		echo "<table border=1 width=100%>\n";
		echo "<tr><td>Имя</td><td>Примечание</td><td>IP</td><td>Редактирование</td><td>Удалить</td></tr>\n";
		$r=mysql_query("SELECT `PCName`, `Notes`, `IP` FROM `pcnames`;");
		for ($i=0; $i<mysql_num_rows($r);$i++)
		{
		echo "<tr>";
		// чередование строк серый - белый
		if ($i%2==0):
			echo "<tr bgcolor=\"grey\">";
		else:
			echo "<tr bgcolor=\"white\">";
		endif;
		$f=mysql_fetch_array($r);

		//если эту строку редактируем
		if ($f[PCName]==$edit):
			echo "<form action=\"it-pc_names.php\" method=\"GET\">\n";
			echo "<td>$f[PCName]<input type=\"hidden\" name=\"PCName\" value=\"$f[PCName]\"></td>";
			echo "<td><input type=\"text\" name=\"Notes\" value=\"$f[Notes]\"></td>";
			echo "<td><input type=\"text\" name=\"IP\" value=\"$f[IP]\"></td>";
			echo "<td><input type=\"submit\" name=\"save_edit\" value=\"Сохранить\"></td>";
		else:
		// те строки, которые не редактируем
		echo "<td>$f[PCName]</td><td>$f[Notes]</td><td>$f[IP]</td><td><a href=\"it-pc_names.php?edit=$f[PCName]\">Редактировать</a></td><td><a href=\"it-pc_names.php?delete=$f[PCName]\">Удалить</a></td>";
		endif;


		echo "</tr>\n";
		}
		echo "</table>";
		echo "</body></html>";
	endif;
else:
	echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=1\"></HEAD><BODY></BODY></HTML>";
endif;
?>