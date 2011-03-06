import logging, email
import sys
import re
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
import return_info
from google.appengine.api import mail
import accounts

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
		logger = logging.getLogger()
		t = mail_message.to
		mobile = mail_message.sender
		subj = mail_message.subject
		bodies = mail_message.bodies('text/plain')
		for body in bodies:
			b = body[1].decode()
		logger.info("From: " + mobile)
		logger.info("To: " + t)
		logger.info(mail_message.date)
		logger.info("Subject: " + subj)
		logger.info("Body: " + b)
		if 'SMS' in subj:
			if 'account' in b.lower():
				reply = accounts.createAccount(mobile,b)
			else:
				reply = return_info.main(b,mail_message.date,True,mobile)
			account = accounts.getAccount(mobile)
			logger.info(reply[0])
			logger.info(reply[1])
			logger.info(account)
			if account != None:
				mail.send_mail(sender = "shuttles.nu@gmail.com",
							to = account,
							subject = reply[0],
							body =  reply[1])

def main():
	application = webapp.WSGIApplication([LogSenderHandler.mapping()],
                                         debug=True)
	run_wsgi_app(application)
	
if __name__ == '__main__':
    main()