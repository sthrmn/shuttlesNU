import sys
import re

def parseLine(line):
	parsed = []
	s = ''
	a = 0
	for c in line:
		if c != '\t':
			s = s + c
		else:
			if ':' in s:
				s = re.match('(\d+):(\d+)',s)
				h = int(s.group(1))
				m = int(s.group(2))
				if h == 12:
					a = 12
				else:
					h = h + a
				s = (h,m)
			parsed.append(s)
			s = ''
	return parsed

def main(StopNumbers,South,North):
	f = open('shuttletimessouth.txt','r')
	i = 0
	for line in f:
		parsed = parseLine(line)
		South[parsed[0]] = parsed[1:-1]
		StopNumbers[parsed[0]] = i
		i = i + 1
	f.close()
		
	f = open('shuttletimesnorth.txt','r')
	for line in f:
		parsed = parseLine(line)
		North[parsed[0]] = parsed[1:-1]
	f.close()
	

if __name__ == '__main__':
    main()