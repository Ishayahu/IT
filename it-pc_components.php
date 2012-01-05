<?
echo "<html>\n<head>\n<title>MySQL IT DB - Состав компьютеров</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
mysql_connect("","","");
mysql_query("set names utf8");
mysql_select_db("it");
//выбор компьютера
if (isset($_GET['PCName'])):
$PCName=$_GET['PCName'];
else:
$PCName='0';
endif;
// меню выбора
echo "<form action=\"it-pc_components.php\" method=\"GET\">\n<select name=\"PCName\" size=1>\n";
$r=mysql_query("SELECT `PCName` FROM `pcnames`;");
for ($i=0; $i<mysql_num_rows($r);$i++)
{
$f=mysql_fetch_array($r);

if ($f[PCName]==$PCName):
echo "<option selected value=$f[PCName]>$f[PCName]</option>\n";
else:
echo "<option value=$f[PCName]>$f[PCName]</option>\n";
endif;
}
echo "</select>\n<input type=\"submit\" name=\"go\" value=\"Select\">\n<input 
type=\"reset\" name=\"b2\" value=\"Reset\">\n</form>\n";

echo "<table border=1 width=100%>\n";
echo "<td>Тип</td><td>№Актива</td><td>Модель</td><td>Серийный номер</td><td>Статус</td><td>№ Гарантии</td><td>Гарантия до:</td></tr>\n";
$r=mysql_query("SELECT `ac`.`Name`,`a`.`AssetNumber`,`a`.`Model`,`a`.`SerialNumber`,`st`.`StatusName`,`a`.`GarantyNumber`,DATE_ADD(`a`.`ByeDate`, INTERVAL `a`.`Garanty` MONTH) `GarantyEnd` FROM `assets` `a` INNER JOIN `assetcategory` `ac` ON `a`.`AssetCategoryNumber`=`ac`.`AssetCategoryNumber` INNER JOIN `statuses` `st` ON `a`.`StatusCode`=`st`.`StatusCode` WHERE `a`.`PCName`='$PCName';");


for ($i=0; $i<mysql_num_rows($r);$i++)
{
// чередование строк серый - белый
if ($i%2==0):
	echo "<tr bgcolor=\"grey\">";
else:
	echo "<tr bgcolor=\"white\">";
endif;
$f=mysql_fetch_array($r);

echo "<td>$f[Name]</td><td>$f[AssetNumber]</td><td>$f[Model]</td><td>$f[SerialNumber]</td><td>$f[StatusName]</td><td>$f[GarantyNumber]</td><td>$f[GarantyEnd]</td>";

echo "</tr>\n";
}
echo "</table></body></html>";
