#ToBigram.py
#parse text to bigram
import linecache

#paramter
limit = 7580 #annotation length

#test
linenum = input('choose an annotation line(<7500):')
if linenum > limit:
	linenum = limit
i = 0
annotation = linecache.getline('../mengniu/annotation.dat',linenum+1)
print 'annotation:', annotation
#cls for class
#spos for short(pattern) file position; 
#lpos for long(full text) file position;
cls, spos, lpos = annotation.split()

#get text
cls = int(cls)
print 'class:',cls
stxt = linecache.getline('../mengniu/pattern.dat',int(spos)*2+1)
print 'pattern text:\n', stxt
ltxt = linecache.getline('../mengniu/mengniu.dat',int(lpos)*2+2)
print 'full text:\n', ltxt

#ignore all ascii char 
ltxtlst = list(ltxt)
for i in range(len(ltxtlst)):
	if ord(ltxtlst[i]) < 128:
		ltxtlst[i] = ' '
ltxt = ''.join(ltxtlst)
print 'ignore ascii:\n',ltxt

#split
bigram = {}
ltxtlst = ltxt.split()
for i in ltxtlst:
	print '\n',i
	for j  in range(len(i)/3-1):
		bi = i[j*3:j*3+6]
		print bi
		bigram[bi] = 1

#
print bigram
#linecache.clearcache()