import smtplib
from email.message import EmailMessage

from_email_addr ="loadsensor@outlook.com"
from_email_pass = "rjvsmgtogdogvxih"#input("please enter your password") #Here is the app password####################################
to_email_addr ="romer.smartlink@gmail.com"

msg = EmailMessage()

body ="Hello from Raspberry Pi"
msg.set_content(body)

msg['From'] = from_email_addr
msg['To'] = to_email_addr

msg['Subject'] = 'TEST TO SEND EMAIL'

server = smtplib.SMTP('smtp.office365.com', 587)

server.starttls()

server.login(from_email_addr, from_email_pass)

server.send_message(msg)

print('Email sent')

server.quit()