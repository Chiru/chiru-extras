import math
import csv
from collections import Counter 

dataset=csv.reader(open('directions2.csv'), delimiter=',')

#for row in dataset: print row

def vectorcreate():
	rows=[]
	for row in dataset:
		features=[]
		ftrs=row[0:6]
		for f in ftrs:
			features.append(int(f))
		label=row[6]
		rows.append({'features':features,'label':label})
	return rows

data=vectorcreate()

#print actionlist[0:20]

def euclidean(v1,v2):
	d=0.0
	for i in range(len(v1)):
		d+=(v1[i]-v2[i])**2
	return math.sqrt(d)


#print data[0]['features'],data[873]['features']
#distance=euclidean(data[0]['features'],data[868]['features'])
#print ('Distance between ',data[0]['label'],' and ',data[868]['label'],' is: ',distance)

def getdistances(data,vec1):
	distancelist=[]
	for i in range(len(data)):
		vec2=data[i]['features']
		distancelist.append((euclidean(vec1,vec2),i))
	distancelist.sort()
	return distancelist

def knnestimate(data,vec1,k=3):
	#Get sorted distances
	dlist=getdistances(data,vec1)
	#avg=0.0
	classy=[]

	#Take the average of the top k results
	for i in range(k):
		idx=dlist[i][1]
		#avg+=data[idx]['label']
		classy.append(data[idx]['label'])
	#avg=avg/k
	#return avg
	estimate = Counter(classy)
	result = estimate.most_common(1)[0]
	return result

classification=knnestimate(data,data[0]['features'])

print classification
