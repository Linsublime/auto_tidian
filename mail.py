#!/usr/bin/env python
# coding=utf-8
__author__ = 'root'
 
import os
import smtplib
import datetime
from email.mime.text import MIMEText
 
class Mail_Model:
 
    def __init__(self):
        self.mail_host = "smtp.qq.com"
        self.mail_user = "yu@oddsfair.cn"
        self.mail_pass = "d301d301"
        self.postfix = "qq.com"
 
    def send_mail(self, to_list, sub, content):
        me = "yu@oddsfair.cn"
        msg = MIMEText(content, _subtype = 'html', _charset = 'utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ';'.join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False
 
# mailto_list=["yu@oddsfair.cn"]
mailto_list=["yu@oddsfair.cn","362731546@qq.com","f@oddsfair.cn" ]
 
mail = Mail_Model()
if mail.send_mail(mailto_list,datetime.datetime.now().strftime('%Y-%m-%d')+ ' 自动生成提点',os.popen('python auto_tidian.py').read()):
    print "发送成功"
else:
    print "发送失败"