from email.mime.multipart import MIMEMultipart
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def func(user, passw, target, message, subject):
    mes = MIMEMultipart()
    mes["From"] = "Me"
    mes["To"] = target
    mes["Subject"] = subject

    body = MIMEText(message, "plain")
    mes.attach(body)

    try:
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login(user, passw)
        mail.sendmail(mes["from"], mes["To"], mes.as_string())
        mail.close()
    except:
        sys.stderr.write("Failed....")
        sys.stderr.flush()


func("yavuzbektas@gmail.com", "160913nb", "ybektas@iaosb.org.tr", "bugün nasılsın", "deneme mesajı")
