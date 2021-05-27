import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

config = configparser.ConfigParser()
config.read("./config.yaml")

sEmail = config['sender']['email']
sPass = config['sender']['password']
sHost = config['sender']['host']
sPort = config['sender']['port']

rEmails = config['reciever']['email_list']
rEmails = rEmails.split(',')

# set up the SMTP server
s = smtplib.SMTP_SSL(host=sHost, port=int(sPort))
s.login(sEmail,sPass)

for email in rEmails:
    #send mail
    msg = MIMEMultipart()       # create a message

    message = "this is a alert test part 2"

    # setup the parameters of the message
    msg['From']=sEmail
    msg['To']=email
    msg['Subject']="ALERT TEST"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)

    del msg