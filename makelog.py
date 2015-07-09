#makelog.py
import time

#
file_annotation = open('../mengniu/annotation.dat','r+')
file_pattern = open('../mengniu/pattern.dat','r')
file_log = open('../mengniu/annotation.log','r+')

position = 0
count = 0
annotation = file_annotation.readline()
file_pattern.readline()
file_pattern.readline()
while annotation != '':
	position = file_pattern.tell()
	count = int(annotation.split()[1])
	annotation = file_annotation.readline()
	file_pattern.readline()
	file_pattern.readline()

file_log.read()
file_log.write('%d %d %s\n' % (count+1,position,time.ctime()))

file_log.close()
file_pattern.close()
file_annotation.close()