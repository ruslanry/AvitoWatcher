# -*- coding: utf-8 -*-
import urllib.request
import lxml.html as html
from urllib.parse import quote
import re
import pickle
import datetime
import time
import ftplib
import tomail

host = "185.84.108.232"
ftp_user = "f87614"
ftp_password = "99868555"


BASE_URL = 'https://www.avito.ru'
#first_page = '/pyt-yah/kvartiry/prodam?p=1&s=101'
#first_page = '/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?s=101&metro=160-164-165-176-180-185-187-188-191-199-201-202-205-206-210-1015-1016&f=550_5702-5703-5704'
first_page = '/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?pmax=35000&pmin=0&s=101&metro=156-157-160-164-165-166-168-171-176-180-183-185-187-188-189-190-191-192-199-201-202-203-205-206-209-210-1015-1016&f=550_5703-5704-5705'

pickle_file_name = 'data.piclle'
id_file_name     = 'data.id.piclle'

def toFTP(filename):
    con = ftplib.FTP(host, ftp_user, ftp_password)
    try:
        # Открываем файл для передачи в бинарном режиме
        f = open("html/"+filename, "rb")
        # Передаем файл на сервер
        send = con.storbinary("STOR "+ "/ryfotoru/avito/" +filename, f)
    except FileNotFoundError:
        print("No file "+filename)
    finally:
        # Закрываем FTP соединение
        con.close

def clearStr(rawStr):
    #re.sub(r'\s', '', rawStr)
    #re.sub(r'\n', '', rawStr)
    return rawStr.strip()

def getData(element):
    ret = {}
    ret['id']     = element.xpath(".//@id")[0]
    ret['name']   = clearStr("".join(element.xpath(".//div[1]/h3/a/text()")))
    ret['price']  = clearStr("".join(element.xpath(".//*[@class='about']/text()")))
    ret['link']   = clearStr("".join(element.xpath(".//div[1]/h3/a/@href")))
    ret['img']    = clearStr("".join(element.xpath(".//*[@class='photo-count-show']/@src")))
    ret['addres'] = clearStr("".join(element.xpath(".//*[@class='address fader']/text()")))
    ret['metro']  = clearStr("".join(element.xpath(".//*[@class='address fader']/text()")[1]))
    ret['dst']    = clearStr("".join(element.xpath(".//*[@class='address fader']/span/text()")))
    ret['date']   = date
    ret['img']    = ret['img'].replace('//', 'http://')
     
    #print(ret['img'])
    try:
        dst  = ret['dst'].split(' ')
        if (dst[1]=='км'):
            ret['dstm'] = int(float(dst[0])*1000)
        else:
            ret['dstm'] = int(float(dst[0])*1)
    except Exception:
            print(dst)
            ret['dstm'] = 0
            
    name = re.match(r"(?P<room>.*?)-к квартира, (?P<pl>.*?) м², (?P<fl>.*?) эт.",ret['name'])
    if name:
        ret['roomcnt'] = name.group('room')
        ret['pl']      = name.group('pl')
        ret['fl']      = name.group('fl')
    else:
        name = re.match(r"(?P<room>Студия), (?P<pl>.*?) м², (?P<fl>.*?) эт.",ret['name'])
        if name:
            ret['roomcnt'] = name.group('room')
            ret['pl']      = name.group('pl')
            ret['fl']      = name.group('fl')
        else:
            ret['roomcnt'] = '0'
            ret['pl']      = '0'
            ret['fl']      = '0\0'
            

    price = re.match(r"(?P<price>.*?) руб.",ret['price'])
    if price:
        ret['price'] = int("".join(price.group('price').split()))
        
    return ret


def loadFromNet():
    print('load from net')
    html_data=html.parse(urllib.request.urlopen(BASE_URL + first_page))
    all_page = html_data.xpath(".//*[@class='pagination-page']/@href")[:]
    all_page.append(first_page)
    u = set()
    for p in all_page:
        u.add(p)
    all_page = list(u)

    data = []

    for page in all_page:
        print(page)
        time.sleep(1)
        html_data=html.parse(urllib.request.urlopen(BASE_URL + page))
        new_page = html_data.xpath(".//*[@class='pagination-page']/@href")[:]
        for np in new_page:
            if (np not in u):
                u.add(np)
                all_page.append(np)
        try:
            all_elements = html_data.xpath(".//*[@data-type]")
        except IndexError:
            all_elements = []

        for element in all_elements:
            data.append(getData(element))
        
    return data
    
def saveToFile(fname,data):
    with open(fname, 'wb') as f:
        pickle.dump(data, f,protocol=2)
    

def loadDataId(fname):
    try:
        with open(fname, 'rb') as f:
            ret = pickle.load(f)
    except FileNotFoundError:
        print('error load ID from File')
        ret = set()
        saveToFile(fname,ret)
    return ret

def saveTextFile(fname,saveData):
    if len(saveData)<1:
        return 0
    f = open(fname, "w")
    f.write("date\tid\tname\tprice\taddres\tmetro\tdst\troomcnt\tpl\tfl\timg\tlink\n")
    for d in saveData:
        d['url']=BASE_URL
        s = '%(date)s\t%(id)s\t%(name)s\t%(price)s\t%(addres)s\t%(metro)s\t%(dst)s\t%(roomcnt)s\t%(pl)s\t%(fl)s\t%(url)s%(img)s\t%(url)s%(link)s\n' % d
        f.write(s)
    f.close()

def saveHTMLFile(fname,saveData):
    if len(saveData)<1:
        return 0
    
    #blank = open('_blank.html', 'r')
    with open("html/"+'_blank.html', 'r') as myfile:
        blank=myfile.read().replace('\n', '')

    #news = '%(date)s\t%(id)s\t%(name)s\t%(price)s\t%(addres)s\t%(metro)s\t%(dst)s\t%(roomcnt)s\t%(pl)s\t%(fl)s\t%(url)s%(img)s\t%(url)s%(link)s\n' % d
    s = '<tr><td class="success">...</td></tr>'
    s = ''
     
    for d in saveData:
        if (d['price']>=40000):
            d['class'] = 'danger'
        elif (d['price']>=30000):
            d['class'] = 'warning'
        elif (d['price']>=25000):
            d['class'] = 'info'
        elif (d['price']>=18000):
            d['class'] = 'success'
        elif (d['price']>=0):
            d['class'] = 'active'
        
        d['url']=BASE_URL
        news = '<tr class="%(class)s"><td><a href="%(url)s%(link)s" target="_blank">%(name)s</a><br><span class="badge">%(metro)s</span>%(dst)s<br><small><a href="https://yandex.ru/images/search?url=%(img)s&rpt=imageview" target="_blank">%(addres)s</a></small></td><td>%(price)s</td><td><img src="%(img)s" class="thmb"></td></tr>' % d
        s    = s+news
    
    dataHtml = blank.replace('{DATA}', s)
    
    f = open(fname+'.html', "w")
    f.write(dataHtml)
    f.close()

def toMail(sendData):
    if len(sendData)<1:
        return 0
        
    msg_txt = ''
    for d in sendData[:20]:
        d['url']=BASE_URL
        news    = '%(name)s \t %(price)s \t %(metro)s \t %(dst)s \t %(url)s%(link)s \n' % d
        msg_txt = msg_txt+news
    
    if len(sendData)>20:
        msg_txt = msg_txt+'Показано первые 20 предложений.'
    
    msg_txt = msg_txt+'\n\n\n http://avito.ryfoto.ru/last_new.html'
    fromaddr = 'Avito Parser <admin@ughpy.ru>'
    toaddr   = 'Ruslan.Ry <ruslan.ry@gmail.com>'
    subj     = 'Квартиры '+dt
    msg_txt  = msg_txt
    
    tomail.sendEmail(fromaddr, toaddr, subj, msg_txt)


now  = datetime.datetime.now()
date = now.strftime("%Y-%m-%d") 
print(date)
newfile = now.strftime("%Y-%m-%d.%H:%M.New.txt") 
dt      = now.strftime("%Y-%m-%d.%H:%M") 

all_id   = loadDataId(id_file_name)
all_data = loadFromNet()
new_data = []

for d in all_data:
    if (d['id'] not in all_id):
        all_id.add(d['id'])
        new_data.append(d)

all_data = sorted(all_data, key=lambda sdata: sdata['dstm'])
new_data = sorted(new_data, key=lambda sdata: sdata['dstm'])

saveToFile(id_file_name,all_id)
saveTextFile("text/_all.txt",all_data)
#saveTextFile("text/_last_new",new_data)
#saveTextFile("text/"+newfile,new_data)
saveHTMLFile("html/index",all_data)
saveHTMLFile("html/last_new",new_data)
#saveHTMLFile("html/"+newfile,new_data)

toFTP("index.html")
toFTP("last_new.html")
#toFTP(newfile+".html")

toMail(new_data)

