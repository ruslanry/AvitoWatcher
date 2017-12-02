import ftplib
host = "185.84.108.232"
ftp_user = ""       #Имя FTP
ftp_password = ""   #Пароль FTP
filename = "_all.txt"
 
con = ftplib.FTP(host, ftp_user, ftp_password)
# Открываем файл для передачи в бинарном режиме
f = open("text/"+filename, "rb")
# Передаем файл на сервер
send = con.storbinary("STOR "+ "/ryfotoru/avito/" +filename, f)
# Закрываем FTP соединение
con.close
