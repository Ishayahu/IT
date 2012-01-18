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
		echo "<html>\n<head>\n<title>MySQL IT DB - Ремонт активов</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
		mysql_connect("46.254.16.220","it","planrabot");
		mysql_query("set names utf8");
		mysql_select_db("it");
		//выбор компьютера
		if (isset($_GET['AssetNumber'])):
		$AssetNumber=mysql_escape_string($_GET['AssetNumber']);
		else:
		$AssetNumber='0';
		endif;
		// меню выбора
		echo "<form action=\"it-remonts.php\" method=\"GET\">\n<select name=\"AssetNumber\" size=1>\n";
		$r=mysql_query("SELECT `a`.`AssetNumber`,`ac`.`Name` FROM `assets` `a` INNER JOIN `assetcategory` `ac` ON `a`.`AssetCategoryNumber`=`ac`.`AssetCategoryNumber` WHERE `ac`.`AssetCategoryNumber` not in (1,20,7,19,22,27,30,33,36,37,35,34,44,45,5,10,13,18,6,8,21,26);");
		for ($i=0; $i<mysql_num_rows($r);$i++)
		{
		$f=mysql_fetch_array($r);

		if ($f[AssetNumber]==$AssetNumber):
		echo "<option selected value=$f[AssetNumber]>$f[AssetNumber]($f[Name])</option>\n";
		else:
		echo "<option value=$f[AssetNumber]>$f[AssetNumber]($f[Name])</option>\n";
		endif;
		}
		echo "</select>\n<input type=\"submit\" name=\"go\" value=\"Select\">\n<input 
		type=\"reset\" name=\"b2\" value=\"Reset\">\n</form>\n";

		echo "<table border=1 width=100%>\n";
		echo "<td>№пп</td><td>Поломка</td><td>Фирма</td><td>Начало ремонта</td><td>Конец ремонта</td><td>Гарантия до:</td><td>Стоимость</td><td>№ Гарантии</td></tr>\n";
		$r=mysql_query("SELECT `ID`, `Breakdown`, `DistributorName`, `StartDate`, `EndDate`, DATE_ADD(`EndDate`, INTERVAL `Garanty` MONTH) `GarantyEnd`, `Price`, `GarantyNumber` FROM `repairing` WHERE `AssetNumber`='$AssetNumber';");


		for ($i=0; $i<mysql_num_rows($r);$i++)
		{
		// чередование строк серый - белый
		if ($i%2==0):
			echo "<tr bgcolor=\"grey\">";
		else:
			echo "<tr bgcolor=\"white\">";
		endif;
		$f=mysql_fetch_array($r);

		echo "<td>$f[ID]</td><td>$f[Breakdown]</td><td>$f[DistributorName]</td><td>$f[StartDate]</td><td>$f[EndDate]</td><td>$f[GarantyEnd]</td><td>$f[Price]</td><td>$f[GarantyNumber]</td></tr>\n</td>";

		echo "</tr>\n";
		}
		echo "</table></body></html>";
	endif;
else:
	echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=1\"></HEAD><BODY></BODY></HTML>";
endif;
?>