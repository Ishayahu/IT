<?
mysql_connect("46.254.16.220","it","planrabot");
mysql_query("set names utf8");
mysql_select_db("it");
//если введены данные
if (isset($_GET['enter']) and $_GET['enter']=="Вход" and isset($_GET['password']) and isset($_GET['user'])):
	$user=$_GET['user'];
	$password=md5($_GET['password']);
	$r=mysql_query("SELECT `password` FROM `users` WHERE `login`='$user';");
	$f=mysql_fetch_array($r);
	if ($f[password]==$password):
		// создание куки с логином и паролем
		//echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=it-set_cookie.php?user=$user&$password=asdf\"></HEAD><BODY></BODY></HTML>";
		SetCookie("$user","$password");
	else:
		echo "Логин или пароль неверен!";
	endif;
else:
	echo "<html>\n<head>\n<title>MySQL IT DB - Вход</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
	echo "<form action=\"index.php\" method=\"GET\">\nЛогин:<input type=\"text\" name=\"user\" value=\"\">\n<br>Пароль<input type=\"password\" name=\"password\" value=\"\">\n<input type=\"submit\" name=\"enter\" value=\"Вход\">";
endif;
	echo "</body></html>";
?>
