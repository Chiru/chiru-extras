from svmutil import *
import csv
import numpy as np
svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

dataset=csv.reader(open('directions.csv'), delimiter=',')

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
	if row[6]=='Left':
		labels.append(float(1))
	if row[6]=='Right': 
		labels.append(float(2))
	if row[6]=='Forwards': 
		labels.append(float(3))
	if row[6]=='Backwards': 
		labels.append(float(4))
	#labels.append(row[6])
#print features
#print labels

#answers,inputs = [data[r][label] for r in data],[data[r][features] for r in data]  

a = np.asarray(features)

a /= np.max(np.abs(a),axis=0)
feat = a.tolist()
#print feat

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