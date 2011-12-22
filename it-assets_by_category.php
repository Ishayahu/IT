<?
echo "<html>\n<head>\n<title>MySQL IT DB - Активы по категориям</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
mysql_connect("46.254.16.220","it","planrabot");
mysql_query("set names utf8");
mysql_select_db("it");
//выбор категории активов
if (isset($_GET['cat'])):
$cat=$_GET['cat'];
else:
$cat=0;
endif;
// обработка редактирования
if (isset($_GET['edit'])):
$edit=$_GET['edit'];
else:
$edit=-1;
endif;

if (isset($_GET['save']) and $_GET['save']=="Сохранить"):
	$StatusCode=$_GET['StatusCode'];
	$AssetNumber=$_GET['AssetNumber'];
	$Place=$_GET['Place'];
	$PCName=$_GET['PCName'];
	$r=mysql_query("UPDATE `assets` SET `StatusCode`=$StatusCode,`Place`='$Place',`PCName`='$PCName' WHERE `AssetNumber`=$AssetNumber;");
	echo "Done: UPDATE `assets` SET `StatusCode`=$StatusCode,`Place`='$Place',`PCName`='$PCName' WHERE `AssetNumber`=$AssetNumber;\nResilt: $r";
endif;


echo "<form action=\"it-assets_by_category.php\" method=\"GET\">\n<select name=\"cat\" size=1>\n";
$r=mysql_query("SELECT `AssetCategoryNumber`,`Name` test FROM `assetcategory`;");
for ($i=0; $i<mysql_num_rows($r);$i++)
{
$f=mysql_fetch_array($r);

if ($f[AssetCategoryNumber]==$cat):
echo "<option selected value=$f[AssetCategoryNumber]>$f[test]</option>\n";
else:
echo "<option value=$f[AssetCategoryNumber]>$f[test]</option>\n";
endif;
}
echo "</select>\n<input type=\"submit\" name=\"go\" value=\"Select\">\n<input 
type=\"reset\" name=\"b2\" value=\"Reset\">\n</form>\n";

echo "<table border=1 width=100%>\n";
echo "<td>№</td><td>Модель</td><td>Серийный номер</td><td>Статус</td><td>№ Гарантии</td><td>Место</td><td>№ Компьютера</td><td>Редактирование</td></tr>\n";
$r=mysql_query("SELECT `a`.`Model`,`s`.`StatusName`,`a`.`PCName`,`a`.`Place`,`a`.`SerialNumber`,`a`.`AssetNumber`,`a`.`GarantyNumber` FROM `assets` `a` INNER JOIN `statuses` `s` ON `a`.`StatusCode`=`s`.`StatusCode` WHERE `a`.`AssetCategoryNumber`=$cat AND `a`.`StatusCode`<>5;");
for ($i=0; $i<mysql_num_rows($r);$i++)
{
// чередование строк серый - белый
if ($i%2==0):
	echo "<tr bgcolor=\"grey\">";
else:
	echo "<tr bgcolor=\"white\">";
endif;
$f=mysql_fetch_array($r);


if ($f[AssetNumber]==$edit):
	echo "<form action=\"it-assets_by_category.php\" method=\"GET\">\n";
	echo "<td>$f[AssetNumber]<input type=\"hidden\" name=\"AssetNumber\" value=\"$f[AssetNumber]\"><input type=\"hidden\" name=\"cat\" value=\"$cat\"></td>";
	echo "<td>$f[Model]</td><td>$f[SerialNumber]</td>";
	$StatusCode=mysql_query("SELECT `StatusCode`, `StatusName` FROM `statuses`;");
		echo "<td><select name=\"StatusCode\" size=1>\n";
		for ($x=0; $x<mysql_num_rows($StatusCode);$x++)
		{
		$y=mysql_fetch_array($StatusCode);
		echo "<option value=$y[StatusCode]>$y[StatusName]</option>\n";
		}
	echo "</select></td>\n<td>$f[GarantyNumber]</td>";
	echo "<td><input type=\"text\" name=\"Place\" value=\"$f[Place]\"></td>";
	$PCName=mysql_query("SELECT `PCName` FROM `pcnames`;");
		echo "<td><select name=\"PCName\" size=1>\n";
		echo "<option value=''></option>\n";
		for ($x=0; $x<mysql_num_rows($PCName);$x++)
		{
		$y=mysql_fetch_array($PCName);
		echo "<option value=$y[PCName]>$y[PCName]</option>\n";
		}
	echo "<td><input type=\"submit\" name=\"save\" value=\"Сохранить\"></td>";
else:
echo "<td>$f[AssetNumber]</td><td>$f[Model]</td><td>$f[SerialNumber]</td><td>$f[StatusName]</td><td>$f[GarantyNumber]</td><td>$f[Place]</td><td>$f[PCName]</td><td><a href=\"it-assets_by_category.php?edit=$f[AssetNumber]&cat=$cat\">Редактировать</a></td>";
endif;


echo "</tr>\n";
}
echo "</table></body></html>";
