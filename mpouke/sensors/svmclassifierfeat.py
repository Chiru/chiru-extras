from svmutil import *
import csv
import numpy as np
svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

dataset=csv.reader(open('shortfeatures3dof.csv'), delimiter=',')

features=[]
labels=[]

for row in dataset:
	if len(row)==40:
		ftrs=row[0:39]	
		iftrs=[]
		for f in ftrs:
			iftrs.append(float(f))
		features.append(iftrs)
		if row[-1]=='Still': 
			labels.append(float(0))
		if row[-1]=='PushLeft':
			labels.append(float(1))
		if row[-1]=='PushRight': 
			labels.append(float(2))
		if row[-1]=='PushForwards': 
			labels.append(float(3))
		if row[-1]=='PushBackwards': 
			labels.append(float(4))
		if row[-1]=='LargeCircleRight': 
			labels.append(float(5))
		if row[-1]=='LargeCircleLeft': 
			labels.append(float(6))
		#labels.append(row[6])
#print len(features)
#print len(labels)


#def findminmax(rows):
#	low=[9999999.0]*len(rows)
#	high=[-99999999.0]*len(rows)
#	#Find the lowest and highest values
#	for row in rows:
#		d=row.data
#		for i in range(len(d)):
#			if d[i]<low[i]: low[i]=d[i]
#			if d[i]>high[i]: high[i]=d[i]

	#Create a function that scales input data
	#def scaleinput(d):
		#return [(d.data[i]-low[i])/(high[i]-low[i]) for i in range (len(low))]

	#Scale all the data
	#newrows=[matchrow(scaleinput(row.data)+[row.match]) for row in rows]

	#Return the data and the function
	#return newrows,scaleinput
#print features
hi = max(features)
lo = min(features)
print hi
print lo

#def scaleinput(input):
#	gesture=[]
#	for i in range (len(input)):
#		gesture.append(i/hi)
#	return gesture

a = np.asarray(features)

a /= np.max(np.abs(a),axis=0)
feat = a.tolist()
print feat
#answers,inputs = [data[r][label] for r in data],[data[r][features] for r in data]  

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
	#gesture = scaleinput(iline)
	#print gesture
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
