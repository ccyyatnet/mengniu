#mengniu_annotation.py
import linecache
import time

###parameters
limit = 1000000

###functions
def fetch_keywords(addr):
	file_keywords = open(addr,'r')
	keywords = file_keywords.readline().split('|')
	#for i in keywords:	
	#	print i
	file_keywords.close()
	return keywords

def annotate(content):
	print content
	annotation = raw_input('Is this related?(press ENTER if yes;! to EXIT):')
	if annotation == '!':
		return -1
	else:
		return int(len(annotation)==0)

###main

#keywords = fetch_keywords('../mengniu/keywords.dat')

file_annotation = open('../mengniu/annotation.dat','r+')
file_pattern = open('../mengniu/pattern.dat','r')
file_log = open('../mengniu/annotation.log','r+')

count = 0 #the num of already done
position = 0 #the position of the next to be anno

#load log
log = file_log.readline()
while log!='':
	log_content = log.split(' ')
	count = int(log_content[0])
	position = int(log_content[1]) 
	log = file_log.readline()
#load next
file_annotation.read()
file_pattern.seek(position)
content = file_pattern.readline()
content_pos = file_pattern.readline()

while content!='' and count < limit:
	#annotate
	print linecache.getline('../mengniu/mengniu.dat',int(content_pos)*2+2)
	annotation = annotate(content)
	#exit from middle
	if annotation < 0:
		break
	#save annotation
	file_annotation.write('%d %d %s' % (annotation,count,content_pos))
	print '***** pattern %d is done *****' % count
	#load next
	position = file_pattern.tell()
	content = file_pattern.readline()
	content_pos = file_pattern.readline()
	count+=1

#exit from end
print 'EXITING...\nWrite log:\n%d %d %s\n' % (count,position,time.ctime())
file_log.write('%d %d %s\n' % (count,position,time.ctime()))

file_log.close()
file_pattern.close()
file_annotation.close()

