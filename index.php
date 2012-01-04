<?
mysql_connect("46.254.16.220","it","planrabot");
mysql_query("set names utf8");
mysql_select_db("it");
//если введены данные
if (isset($_GET['enter']) and $_GET['enter']=="Вход" and isset($_GET['password']) and isset($_GET['user'])):
	$user=mysql_escape_string($_GET['user']);
	$password=md5(mysql_escape_string($_GET['password']));
	$r=mysql_query("SELECT `password` FROM `users` WHERE `login`='$user';");
	$f=mysql_fetch_array($r);
	if ($f[password]==$password):
		// создание куки с логином и паролем
		$token=md5($user.date( 'Y-m-d H:i:s', time() ));
		$start=date( 'Y-m-d H:i:s', time() );
		if (SetCookie("token","$token")):
			$r=mysql_query("INSERT INTO `tokens`(`token`, `login`, `start`, `end`) VALUES ('$token','$user','$start',DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 15 MINUTE));");
			echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index2.php\"></HEAD><BODY></BODY></HTML>";
		else:
			echo "<h3>Cookie установить не удалось! Без куки мы не работаем!</h3>";
		endif;
	else:
		echo "<HTML><HEAD><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"1; URL=index.php?error=0\"></HEAD><BODY></BODY></HTML>";
	endif;
else:
	echo "<html>\n<head>\n<title>MySQL IT DB - Вход</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html\" charset=\"utf8\">\n</head>\n<body>";
	if (isset($_GET['error'])):
		$error=$_GET['error'];
		switch ($error):
			case '0': echo "Логин или пароль неверен!"; break;
			case '1': echo "Вход не был произведён"; break;
			case '2': echo "Дата начала сессии позже, чем текущее время! Возможно, время, установленное на сервере не верное. Войдите еще раз."; break;
			case '3': echo "Сессия была завершена. Войдите еще раз."; break;
		endswitch;
	endif;
	echo "<form action=\"index.php\" method=\"GET\">\nЛогин:<input type=\"text\" name=\"user\" value=\"\">\n<br>Пароль<input type=\"password\" name=\"password\" value=\"\">\n<input type=\"submit\" name=\"enter\" value=\"Вход\"><br><a href=\"it-new_user.php\">Новый пользователь</a>";
endif;
	echo "</body></html>";
?>
