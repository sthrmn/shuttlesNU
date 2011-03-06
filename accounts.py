from google.appengine.ext import db
from google.appengine.api import users
import datetime
import return_info
import re

class NumberAccount(db.Model):
		number = db.StringProperty(required=True)
		txt = db.StringProperty(required=True)
		update = db.DateProperty()

def createAccount(mobile,text):
	text.lower()
	subj = 'Acct: '
	parsed = return_info.parse(text)
	carrier = parsed[1]
	carrier.lower()
	n = re.match('"\((\d+)\)\s(\d+)-(\d+)"',mobile)
	n = n.group(1)+n.group(2)+n.group(3)
	account = NumberAccount.gql("WHERE number = :number", number = n)
	for a in account:
		if a.txt != None:
			return [subj, 'Account already exists']
	if carrier == 'sprint':
		sendto = 'messaging.sprintpcs.com'
	elif carrier == 'verizon':
		sendto = 'vtext.com'
	elif carrier == 'tmobile':
		sendto = 'tmomail.net'
	elif carrier == 'att':
		sendto = 'txt.att.net'
	else:
		return [subj, 'carrier not supported']
	sendto = n + '@' + sendto
	newAccount = NumberAccount(number = n, txt = sendto, update = datetime.datetime.now().date())
	newAccount.put()
	return [subj, 'Account created.']

def getAccount(mobile):
	n = re.match('"\((\d+)\)\s(\d+)-(\d+)"',mobile)
	n = n.group(1)+n.group(2)+n.group(3)
	account = NumberAccount.gql("WHERE number = :number", number = n)
	for a in account:
		if a.txt != None:
			return a.txt