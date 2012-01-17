from svmutil import *
import csv
import numpy as np
svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

dataset=csv.reader(open('shortgestures2.csv'), delimiter=',')

features=[]
labels=[]

for row in dataset:
	if len(row)==7:
		ftrs=row[0:6]	
		iftrs=[]
		for f in ftrs:
			iftrs.append(float(f))
		features.append(iftrs)
		if row[6]=='Still': 
			labels.append(float(0))
		if row[6]=='PushLeft':
			labels.append(float(1))
		if row[6]=='PushRight': 
			labels.append(float(2))
		if row[6]=='PushForwards': 
			labels.append(float(3))
		if row[6]=='PushBackwards': 
			labels.append(float(4))
		if row[6]=='LargeCircleRight': 
			labels.append(float(5))
		if row[6]=='Shake': 
			labels.append(float(6))
		#labels.append(row[6])
#print features
#print labels

a = np.asarray(features)

a /= np.max(np.abs(a))
feat = a.tolist()

#print a
#raw_input("Press enter when done...")
#answers,inputs = [data[r][label] for r in data],[data[r][features] for r in data]  

prob = svm_problem(labels,feat)
param = svm_parameter()
param.kernel_type = RBF
#param.cross_validation = param
param.C = 10
#param.kernel_type = LINEAR
m = svm_train(prob,param)

CV_ACC = svm_train(labels, feat, '-v 10')
print CV_ACC

def classify(iline):
	normi = np.asarray(iline)
	normi /= np.max(np.abs(normi))
	gesture = normi.tolist()
	#z = []
	#z.append(iline)
	#print z
	#xi = (iline)
	#result, acc, val = svm_predict([0]*len(z), iline, m)
	result = m.predict(gesture)
	return result
#print acc
#print val
