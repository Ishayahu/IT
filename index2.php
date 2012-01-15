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
		//echo "(end - now)>0 and (now - start)>0";
		$r=mysql_query("UPDATE `tokens` SET `end`=DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 15 MINUTE) WHERE `token`='$token';");
		echo "<html>
				<head>
					<title>MySQL IT DB</title>
					<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">
				</head>
				<body>
					<a href=\"it-assets_by_category.php\">Активы по типам</a><br>
					<a href=\"it-printer_department.php\">Принтер-департамент</a><br>
					<a href=\"it-assets_category.php\">Категории активов</a><br>
					<a href=\"it-pc_names.php\">Компьютеры</a><br>
					<a href=\"it-pc_components.php\">Состав компьютеров</a><br>		
				</body>
			</html>";
	endif;
else:
	echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=1\"></HEAD><BODY></BODY></HTML>";
endif;
?>