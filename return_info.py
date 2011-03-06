import sys
import re
from time import localtime
import shuttletimeparser

StopNumbers = {}
South = {}
North = {}
shuttletimeparser.main(StopNumbers,South,North)
SouthLocations = {'tech':'SheridanNoyes','fost':'SheridanFoster','ryan':'RyanField','jack':'CentralJackson',
			'noyes':'ShermanNoyes','simp':'ShermanSimpson','emer':'ShermanEmerson',
			'sher':'ChicagoSheridan','mab':'ChicagoSheridan','davis':'ChicagoDavis','green':'ChicagoGreen','main':'ChicagoMain',
			'loyala':'SheridanLoyala','ward':'ArriveWard'}
NorthLocations = {'mab':'TheArch','tech':'TechInstitute','fost':'JacobsCenter','lunt':'JacobsCenter','patt':'PattenGym'}
	
def stopTime(start,end):
	start = StopNumbers[SouthLocations[start]]
	end = StopNumbers[SouthLocations[end]]
	return (5*(end-start),2*(end-start))
	
def sisig(start,end,tom,current_all,dir):
	subj = 'Stay or go?'
	next = shuttle_times(start,1,tom,current_all,dir)
	if next == []:
		return 'Go, no more shuttles'
	n = [next[0]]
	now = current_all[3:5]
	next = next[0]
	next = next[0]*60 + next[1]
	now = now[0]*60 + now[1]
	t = stopTime(start,end)
	if (next - now+t[1]) <= t[0]:
		s = 'Stay, next time at ' + formatTimes(n)
	else:
		s = 'Go, next time at ' + formatTimes(n)
	return [subj, s]
	
def parsetime(t):
	m = re.match('(\w+),\s+(\d+)\s+(\w+)\s+(\d+)\s+(\d+):(\d+):(\d+)',t)
	days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
	day = 0
	while(m.group(1) != days[day]):
		day = day+1
	months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	month = 0
	while(m.group(3) != months[month]):
		month = month+1
	parsedTime = [int(m.group(4)), month, int(m.group(2)), (int(m.group(5))-6)%24, int(m.group(6)), int(m.group(7)), day]
	return parsedTime

def shuttle_times(text,n,tom,current_all,dir):
	if text == 'help':
		return []
	else:
		if tom:
			current_time = [0,0]
		else:
			current_time = current_all[3:5]
		times = []
		if dir == 'n':
			Stops = North
			Locations = NorthLocations
		else:
			Stops = South
			Locations = SouthLocations
		for t in Stops[Locations[text]]:
			if t[0] > current_time[0]:
				times.append(t)
			if t[0] == current_time[0] and t[1] >= current_time[1]:
				times.append(t)
		if (n > len(times)):
			n = len(times)
		return times[0:n]

def parse(text):
	max = 5
	text = text + ' '
	s = ''
	parsed = []
	whitespace = ['\n',' ','\t']
	for c in text:
		if c not in whitespace:
			s = s + c.lower()
		else:
			parsed.append(s)
			s = ''
	for i in range(len(parsed),max):
		parsed.append(False)
	return parsed
		
def formatTimes(times):
	ts = ''
	for t in times:
		h = str(t[0]%12) + ':'
		if t[1] < 10:
			m = '0' + str(t[1])
		else:
			m = str(t[1])
		ts = ts + h + m + ' '
	return ts
	
def formatText(text):
	if 'help' in text.lower():
		subj = 'help'
		s = 'help commands - for keys: keys, format: format, options: options'
	elif 'keys' in text.lower():
		subj = 'keys'
		s = 'tech,fost,ryan,jack,noyes,simp,emer,sher,mab,davis,green,loyala,ward'
	elif 'format' in text.lower():
		subj = 'format'
		s = 'with sisig: start end sisig, without: location # (tom)'
	elif 'options' in text.lower():
		subj = 'opts'
		s = 'preface with sisig, with correct format for "Should I Stay or Should I Go" mode. Tells whether to walk, or wait. append tom to find out stops in the morning'
	else:
		return []
	return [subj, s]
	
def main(text,current_all,textFlag,mobile):
	if textFlag:
		current_all = parsetime(current_all)
	loc = parse(text)
	reply = formatText(text)
	if reply == []:
		if loc[0] == 'sisig':
			reply = sisig(loc[1],loc[2],(loc[-1] == 'tom'),current_all,loc[-2])
		else:
			loc = loc[0:4]
			subj = 'Times'
			times = shuttle_times(loc[0],int(loc[1]),(loc[-1] == 'tom'),current_all,loc[-2])
			reply = formatTimes(times)
			reply = [subj, reply]
	return reply

if __name__ == '__main__':
	text = raw_input('commands: ')
	mobile = '"(954) 558-3546" <13476874888.19545583546.xC5PJwLBNs@txt.voice.google.com>'
	date_time = localtime()
	textFlag = False
	reply = main(text,date_time,textFlag,mobile)
	print reply