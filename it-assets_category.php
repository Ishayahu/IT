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
echo "<tr><td>№</td><td>Модель</td><td>Серийный номер</td><td>Статус</td><td>№ Гарантии</td><td>Место</td><td>№ Компьютера</td></tr>\n";
$r=mysql_query("SELECT `a`.`Model`,`s`.`StatusName`,`a`.`PCName`,`a`.`Place`,`a`.`SerialNumber`,`a`.`AssetNumber`,`a`.`GarantyNumber` FROM `assets` `a` INNER JOIN `statuses` `s` ON `a`.`StatusCode`=`s`.`StatusCode` WHERE `a`.`AssetCategoryNumber`=$cat AND `a`.`StatusCode`<>5;");
for ($i=0; $i<mysql_num_rows($r);$i++)
{
echo "<tr>";
$f=mysql_fetch_array($r);
echo "<td>$f[AssetNumber]</td><td>$f[Model]</td><td>$f[SerialNumber]</td><td>$f[StatusName]</td><td>$f[GarantyNumber]</td><td>$f[Place]</td><td>$f[PCName]</td>";
//echo "<td>1</td><td>2</td>";
echo "</tr>\n";
}
echo "</table></body></html>";
