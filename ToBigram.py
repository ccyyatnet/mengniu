#ToBigram.py
#parse text to bigram
import linecache
import copy
import numpy as np
from sklearn import linear_model, svm

##paramter##
limit = 7580 #annotation length
thresh = 5 #lower bound of bi
#model parameter
C = 1
penalty = 'l1'

###function###
##chinese string to bigram##
def tobigram(txt):

	bigram = {}
	
	##ignore all ascii char##
	txtlst = list(txt)
	for i in range(len(txtlst)):
		if ord(txtlst[i]) < 128:
			txtlst[i] = ' '
	txt = ''.join(txtlst)
	#print 'ignore ascii:\n',txt

	##ignore common chinese symbels
	chssym=['\xef\xbc\x8c','\xe3\x80\x82','\xef\xbc\x81','\xef\xbc\x9f','\xef\xbc\x88','\xef\xbc\x89','\xe2\x80\x98','\xe2\x80\x99','\xe2\x80\x9c','\xe2\x80\x9d','\xef\xbc\x9a']
	for i in chssym:
		txt = txt.replace(i,' ')
	#print txt
	
	##split##
	txtlst = txt.split()
	for i in txtlst:
		#print '\n',i
		for j  in range(len(i)/3-1):
			bi = i[j*3:j*3+6]
			#print bi
			if bi in bigram:
				bigram[bi] += 1
			else:
				bigram[bi] = 1

	return bigram

def showdict(dct):
	for i in dct.keys():
		print i,':',dct[i]
	print 'dict length:',len(dct)

#demo func
def tobigram_demo():
	#test
	linenum = input('choose an annotation line(<7500):')
	if linenum > limit:
		print 'exceed!\nshow line:',limit
		linenum = limit
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

	bigram = tobigram(ltxt)
	print bigram
	showdict(bigram)
	#linecache.clearcache()

def predict_demo(model,dct_):
	txt = raw_input('input text:\n')
	bi_txt = tobigram(txt)
	dct_txt = {}
	for bi in dct_:
		dct_txt[bi]=0
	for bi in bi_txt:
		if bi in dct_txt:
			dct_txt[bi] = bi_txt[bi]
	x = []
	for bi in dct_txt:
		x.append(dct_txt[bi])
	y = model.predict(x)[0]
	print 'Classification Result:',y==1

#####################################################
################## main ###############################
######################################################
#create dict for all bigram
file_sample = open('../mengniu/sample.dat','r')

dct = {}
samples = []
y = []
lines = file_sample.readlines()
for i in range(len(lines)/3):
	sample_dct = tobigram(lines[i*3+2])
	samples.append(copy.deepcopy(sample_dct))
	y.append(int(lines[i*3]))
	#showdict(sample_dct)
	#raw_input('continue?:')
	####dct.update(sample_dct)###
	for bi in sample_dct:
		if bi in dct:
			dct[bi] += sample_dct[bi]
		else:
			dct[bi] = sample_dct[bi]

file_sample.close()
#showdict(dct)

#remove all less than thresh
dct_ = {}
for bi in dct:
	if dct[bi] > thresh:
		dct_[bi] = dct[bi]
#showdict(dct_)

#form training X
print 'preparing training data...'
X = []
for i in range(len(samples)):
	x = []
	dct_x = {}
	for bi in dct_:
		dct_x[bi] = 0
	for bi in samples[i]:
		if bi in dct_x:
			dct_x[bi] = samples[i][bi]
	for bi in dct_x:
		x.append(dct_x[bi])
	X.append(copy.deepcopy(x))

#train
print 'training...'
LR = linear_model.LogisticRegression(C=C, penalty = penalty)
LR.fit(X,y)

#predict
print 'predicting...'
pred = LR.predict(X)
TP = 0 
TN = 0
FN = 0
FP = 0
for i in range(len(pred)):
	if pred[i] == 1:
		if y[i] == 1:
			TP += 1
		else:
			FP += 1
	else:
		if y[i] == 1:
			FN += 1
		else:
			TN += 1
if TP + FP == 0:
	P = 'P div by 0!'
else:
	P = float(TP)/(TP+FP)
if TP+FN == 0:
	R =  'R div by 0!'
else:
	R = float(TP)/(TP+FN)
Accuracy = float(TP+TN)/(TP+TN+FP+FN)
if P+R==0:
	F1 = 'F1 div by 0'
else:
	F1 = float(2*P*R)/(P+R)
print 'Precision:',P
print 'Recall:',R
print 'F1:',F1
print 'Accuracy:',Accuracy

#demo
print 'predict demo:'
predict_demo(LR,dct_)


