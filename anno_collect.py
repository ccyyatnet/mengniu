#collect current statistics of annotation.dat

file_annotation = open('../mengniu/annotation.dat','r')

count = 0
anno = [0,0,0]

annotation = file_annotation.readline()
while annotation != '':
	count += 1
	anno[int(annotation.split()[0])] += 1
	last = annotation.split()[1]
	annotation = file_annotation.readline()

print 'count:',count
print 'last:',last
for i in range(len(anno)):
	print 'class',i,':',anno[i]

file_annotation.close()