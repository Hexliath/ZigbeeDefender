# Send Mail


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class CNotify:
    server = None
    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
   
    def send(self,content):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login("zigbee.defender@gmail.com", "3BQrHe6z1yX4s3DB")

        fromaddr = "you@gmail.com"
        toaddr = "hexliath@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Python email"
        msg.attach(MIMEText(content, 'plain'))

        text = msg.as_string()
        self.server.sendmail(fromaddr, toaddr, text)
        self.server.quit()