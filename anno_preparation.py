#annotation preparation
# -*- coding: utf-8 -*-  
import re

###parameters
limit = 500000
tolerant = 30

###functions
def fetch_keywords(addr):
	file_keywords = open(addr,'r')
	keywords = file_keywords.readline().split('|')
	#for i in keywords:	
	#	print i
	file_keywords.close()
	return keywords

###main
keywords = fetch_keywords('../mengniu/keywords.dat')

file_mengniu = open('../mengniu/mengniu.dat','r')
file_pattern = open('../mengniu/pattern.dat','w')
file_keystat = open('../mengniu/keystat.dat','w')

count = 0
content = 'start'
pattern_dict = {}

key_dict = {}
for key in keywords:
	key_dict[key]=0 

content_type = file_mengniu.readline()
content = file_mengniu.readline()
while content!='' and count < limit:
	#print count,':',content_type,content
	for key in keywords:
		##
		reg = re.compile('.{0,%d}%s.{0,%d}' % (tolerant,key,tolerant))
		match = re.findall(reg,content)
		if len(match):
			#print key,match[0]
			pattern_dict[match[0]]=count
			key_dict[key]+=1
		##
	print count
	content_type = file_mengniu.readline()
	content = file_mengniu.readline()
	count+=1

file_mengniu.close()

###output
print 'num_patterns:',len(pattern_dict)
file_keystat.write('num_patterns:%d\n\n' % len(pattern_dict))
for key in keywords:
	file_keystat.write('%s %d\n' % (key,key_dict[key]))
for pat in pattern_dict.keys():
	file_pattern.write('%s\n%d\n' % (pat,pattern_dict[pat]))

file_pattern.close()
file_keystat.close()