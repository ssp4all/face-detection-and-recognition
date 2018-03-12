import RPi.GPIO as GPIO
import time
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import urllib2
import cookielib
from getpass import getpass
import sys
import os
from stat import *


def take_photo():
	#yaad karne de 
	subprocess.call('/var/www/capture_img.sh')



def send_mail():
	filePath = "/var/www/file.jpg"

    From = 'motionsensor4all@gmail.com'
    To = '2015suraj.pawar@ves.ac.in'
    password = 'motionsensor4all@gmail'
    msg = MIMEMultipart()
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Intruder Alert'
	msg['Date'] = formatdate(localtime=True)

	msg.attach(MIMEText('Someone is waiting'))
	smtp = smtplib.SMTP('smtp.gmail.com:587')
	smtp.starttls()
	smtp.login(From, password)
	ctype, encoding = mimetypes.guess_type(filePath)
	if ctype is None or encoding is not None:
		ctype = 'application/octet-stream'
	maintype, subtype = ctype.split('/', 1)
	fp = open(filePath, 'rb')
	part = MIMEImage(fp.read(), _subtype=subtype)
	fp.close()
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % filePath)
	msg.attach(part)
	smtp.sendmail(From, To, msg.as_string())
	smtp.close()

def send_msg():
	message = "Intruder Alert"
	number = "9892420886"

	if __name__ == "__main__":  
	    username = "9892420886"
	    passwd = "motionsensor"

	    message = "+".join(message.split(' '))

 #logging into the sms site
	    url ='http://site24.way2sms.com/Login1.action?'
	    data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

	 #For cookies

	    cj= cookielib.CookieJar()
	    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	 #Adding header details
	    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
	    try:
	        usock =opener.open(url, data)
	    except IOError:
	        print("error")
	        #return()

	    jession_id =str(cj).split('~')[1].split(' ')[0]
	    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
	    send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
	    opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
	    try:
	        sms_sent_page = opener.open(send_sms_url,send_sms_data)
	    except IOError:
	        print("error")
	        #return()

	print("success")



while(True):
	if GPIO.input(22)==1: 
		take_photo()
		send_mail()
		send_msg()
		time.sleep(30)
	else:
		time.sleep(3)