#!/usr/bin/env python
#encode=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from email.mime.text import MIMEText
import smtplib
# from subprocess import Popen, PIPE
email_server = 'smtp.exmail.qq.com'
warning_account = 'hcyunwei@credithc.com'
warning_account_passwd = 'baiheliangchi2015'


def send_email(receviers, subject, html_content):
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg["From"] = warning_account
    msg["To"] = "".join(receviers)
    msg["Subject"] = u'%s' % subject

    try:
        s = smtplib.SMTP_SSL(email_server, 465)
        s.login(warning_account, warning_account_passwd)
        s.sendmail(warning_account, receviers, msg.as_string())
        s.close()
    except Exception:
        import traceback
        traceback.print_exc()
        pass
    # sender = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    # sender.communicate(msg.as_string())

if __name__ == '__main__':
    send_email(['liyankun160613@credithc.com','845245370@qq.com'], "title", "hello world")
