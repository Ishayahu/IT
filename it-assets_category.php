<?
echo "<html>\n<head>\n<title>MySQL IT DB - Категории активов</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
mysql_connect("46.254.16.220","it","planrabot");
mysql_query("set names utf8");
mysql_select_db("it");
//если новая категория актива
if (isset($_GET['new_cat'])):
$new_cat=$_GET['new_cat'];
$r=mysql_query("INSERT INTO `assetcategory`(`AssetCategoryNumber`, `Name`) VALUES (null,'$new_cat');");
echo "Done: INSERT INTO `assetcategory`(`AssetCategoryNumber`, `Name`) VALUES (null,'$new_cat');\nResilt: $r";
endif;


echo "<form action=\"it-assets_category.php\" method=\"GET\">\n<input type=\"text\" name=\"new_cat\" value=\"$f[puted]\"><input type=\"submit\" name=\"save\" value=\"Сохранить\">";

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
