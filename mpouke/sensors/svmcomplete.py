from svmutil import *
import csv
import numpy as np
import extract as ex
svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

dataset=csv.reader(open('completegestures.csv'), delimiter=',')

features=[]
labels=[]

for row in dataset:
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
	if row[6]=='LargeCircleCW': 
		labels.append(float(5))
	if row[6]=='LargeCircleCCW': 
		labels.append(float(6))
	if row[6]=='TiltLeft': 
		labels.append(float(7))
	if row[6]=='TiltRight': 
		labels.append(float(8))
	if row[6]=='TiltForwards': 
		labels.append(float(9))
	if row[6]=='TiltBackwards': 
		labels.append(float(10))
	if row[6]=='Shake': 
		labels.append(float(11))
	if row[6]=='Grab': 
		labels.append(float(12))
	#labels.append(row[6])
#print features
#print labels

a = np.asarray(features)

a /= np.max(np.abs(a),axis=0)
feat = a.tolist()

#answers,inputs = [data[r][label] for r in data],[data[r][features] for r in data]  
print labels
print feat

print len(labels)
print len(feat)

prob = svm_problem(labels,feat)
param = svm_parameter()
param.kernel_type = RBF
#param.C = 10
#param.kernel_type = LINEAR
m = svm_train(prob,param)

CV_ACC = svm_train(labels, feat, '-v 10')
print CV_ACC

def classify(iline):
	normi = np.asarray(iline)
	normi /= np.max(np.abs(normi),axis=0)
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
