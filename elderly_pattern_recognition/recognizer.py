import pandas as pd
import numpy as np
from collections import Counter,defaultdict
from itertools import compress
from random import choice
import scipy.spatial as sp

ffile = open('svector.txt','r')
flist = ffile.read()
vlist = flist[1:-1].split(',')
fselection = [float(f) for f in vlist]
dataset = pd.read_csv('datatestst.csv', index_col=0, parse_dates=True)
#locations = pd.read_csv('locations.csv', index_col=0, parse_dates=True)
classes = dataset['Annotations']
locations = dataset['Locations']
#print dataset
#features = dataset.drop('Index')
features = dataset._get_numeric_data()
split = len(features)//3
training_data = features[split:]
training_class = classes[split:]
validation_data = features[:split]
validation_class = classes[:split]
labellist = features.columns.tolist()

locdict = defaultdict(list)

def euclidean(v1,v2):
	d=0.0
	for i in range(len(v1)):
		d+=(v1[i]-v2[i])**2
	return np.sqrt(d)

for f in locations.index:
    #print locseries[f]
    if dataset.Annotations[f] in locdict[locations[f]]: continue
    locdict[locations[f]].append(dataset.Annotations[f])

print locdict

def knn(vec1,location,dataset=training_data,k=1):
    dlist = []
    for i in dataset.index:
        if training_class.ix[i] in locdict[location]:
            vec2 = compress(dataset.ix[i],fselection)
            d = (euclidean(vec1,list(vec2)))
            dlist.append([d,i])
        else: dlist.append([999,i])
    #print dlist
    dlist.sort()
    closest = []
    for f in range(k):
        #print range(k)
        #print dlist[f]
        closest.append(classes[dlist[f][1]])
    estimate = Counter(closest)
    result = estimate.most_common(1)
    return result

results = []
for f in validation_data.index:
    location = locations[f]
    #print location
    vec = compress(validation_data.ix[f],fselection)
    vec = list(vec)     
    results.append(knn(vec,location))

score = 0
for x,y in zip(results,validation_class):
    #print x,y
    if x[0][0] == y:
        score = score + 1

    #print float(score)/float(len(results))
print float(score)/float(len(results))
#print results
