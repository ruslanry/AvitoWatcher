# -*- coding: utf-8 -*-
import smtplib
import sys
from email.mime.text import MIMEText
from email.header    import Header

def sendEmail1(fromaddr, toaddr, subj, msg_txt):
    username = '' #Почта отправителя
    password = '' #Пароль

    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % ( fromaddr, toaddr, subj, msg_txt)
     
    server = smtplib.SMTP('cp411.agava.net:587')
    #Выводим на консоль лог работы с сервером (для отладки)
    server.set_debuglevel(1);
    #Переводим соединение в защищенный режим (Transport Layer Security)
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

def sendEmail(fromaddr, toaddr, subj, msg_txt):
    msg = MIMEText(msg_txt, 'plain', 'utf-8')
    msg['Subject'] = Header(subj, 'utf-8')
    msg['From'] = fromaddr
    msg['To']   = toaddr

    s = smtplib.SMTP('cp411.agava.net', 587, timeout=10)
    s.set_debuglevel(1)
    try:
        s.starttls()
        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    finally:
        s.quit()

if __name__ == '__main__':
    fromaddr = 'Ry <admin@ughpy.ru>'
    toaddr = 'Ry <ruslan.ry@gmail.com>'
    subj = 'Notification from system'
    msg_txt = 'проверка'.encode('utf-8')

    sendEmail(fromaddr, toaddr, subj, msg_txt)
