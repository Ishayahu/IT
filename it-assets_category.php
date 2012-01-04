<?
mysql_connect("46.254.16.220","it","planrabot");
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
		echo "<html>\n<head>\n<title>MySQL IT DB - Категории активов</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";

		//если новая категория актива
		if (isset($_GET['new_cat'])):
		$new_cat=mysql_escape_string($_GET['new_cat']);
		$r=mysql_query("INSERT INTO `assetcategory`(`AssetCategoryNumber`, `Name`) VALUES (null,'$new_cat');");
		echo "Done: INSERT INTO `assetcategory`(`AssetCategoryNumber`, `Name`) VALUES (null,'$new_cat');\nResilt: $r";
		endif;


		echo "<form action=\"it-assets_category.php\" method=\"GET\">\n<input type=\"text\" name=\"new_cat\" value=\"\"><input type=\"submit\" name=\"save\" value=\"Сохранить\">";

		echo "<table border=1 width=100%>\n";
		echo "<tr><td>№</td><td>Категория</td></tr>\n";
		$r=mysql_query("SELECT `AssetCategoryNumber`, `Name` FROM `assetcategory`;");
		for ($i=0; $i<mysql_num_rows($r);$i++)
		{
		echo "<tr>";
		$f=mysql_fetch_array($r);
		echo "<td>$f[AssetCategoryNumber]</td><td>$f[Name]</td>";
		echo "</tr>\n";
		}
		echo "</table>";
		echo "</body></html>";
	endif;
else:
	echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=1\"></HEAD><BODY></BODY></HTML>";
endif;
?>