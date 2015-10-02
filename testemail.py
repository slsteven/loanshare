#!/usr/bin/python

import smtplib

sender = ''
receivers = ['kyle.koerber@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message 2 the reconking .
"""

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:25')
   smtpObj.starttls()
   smtpObj.login('loanshare.dojo@gmail.com',"Codingdojo1!")
   smtpObj.sendmail(sender, receivers, message)
   print "Successfully sent email"
except smtplib.SMTPException:
   print "Error: unable to send email"
