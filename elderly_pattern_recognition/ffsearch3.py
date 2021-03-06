import pandas as pd
import numpy as np
from collections import Counter
from itertools import compress
from random import choice
import scipy.spatial as sp

selectionvector = open('svector.txt','w')
dataset = pd.read_csv('datatestst.csv', index_col=0, parse_dates=True)
classes = dataset['Annotations']
#print dataset
#features = dataset.drop('Index')
features = dataset._get_numeric_data()
split = len(features)//3
training_data = features[split:]
training_class = classes[split:]
validation_data = features[:split]
validation_class = classes[:split]
labellist = features.columns.tolist()

def euclidean(v1,v2):
	d=0.0
	for i in range(len(v1)):
		d+=(v1[i]-v2[i])**2
	return np.sqrt(d)

def matrixtest(fvector):

    labels = validation_data.columns.tolist()
    selection = [x for x in compress(labels,fvector)] 
    trainingframe = training_data.ix[:,selection]
    validationframe = validation_data.ix[:,selection]
    testdistances = sp.distance.cdist(trainingframe.values,validationframe.values)
    #print len(validation_class.ix[:])
    #print validation_class.values.shape
    #print 'validation data length', len(validation_data.ix[:])
    #print 'training data shape', training_data.values.shape
    #print 'validation data shape', validation_data.values.shape
    #print "distance matrix shape:", testdistances.shape
    distancematrix = pd.DataFrame(testdistances,index=training_data.index, columns=validation_data.index)
    dmatrixclasses = []
    #print distancematrix
    for f in distancematrix.index:
        goy = min(distancematrix.ix[f])
        #print goy
        #print f.name
        b = (distancematrix.ix[f] == goy)
        #print b
        goee = b.index[b.argmax()]
        dmatrixclasses.append(classes[goee])

    return dmatrixclasses

def score_classifier(results):
    score = 0
    #print len(results)
    #print len(validation_class)
    #print len(training_class)
    #print len(results)
    for x,y in zip(results,training_class):
        #print x,y
	if x == y:
	    score = score + 1

    #print float(score)/float(len(results))
    return float(score)/float(len(results))

def findbest(fselection,direction):
    feature = 0
    #backwards = 0
    #dim = 25
    best = 0.0
    #print fselection
    #print 'Vector length',len(fselection)
    if direction==0:
        for i in xrange(len(fselection)):
            #print 'Onwards', i
	    if fselection[i] == 0:
	        fselection[i] = 1
	        results = matrixtest(fselection)
	        score = score_classifier(results)
	        if score > best:
                    best = score
		    feature = i
		fselection[i] = 0
    else:
        for i in xrange(len(fselection)):
            #print 'Retreat',i
	    if fselection[i] == 1:
	        fselection[i] = 0
	        results = matrixtest(fselection)
	        score = score_classifier(results)
	        if score > best:
                    best = score
		    feature = i
		fselection[i] = 1

    return feature,best

def ffsearch():
    fvector = np.zeros(len(features.columns))
    dim_limit = len(fvector)
    best_result = 0.0
    bestdim = 0
    backwards = 0
    dim = 0
    res_vector = np.zeros(dim_limit)
    print dim_limit
    print len(res_vector)
    print len(fvector)
    while dim <= dim_limit-1:
        print dim
        #print 'forwards'
        best_feature_add, best_result_add = findbest(fvector,backwards)
        fvector[best_feature_add] = 1
        print 'Best results of the moment',fvector,best_result_add 
        #print 'wat'
        if best_result < best_result_add:
            best_result = best_result_add
	    best_fvector = list(fvector)
	    print "Updating best feature vector"
	if best_result_add > res_vector[dim]:
            res_vector[dim] = best_result_add
        print 'Best results on forwards', best_fvector, best_result
        backwards = 1
        while backwards:
            #print 'backwards'
            if dim > 2:
                best_feature_rem,best_result_rem = findbest(fvector,backwards)
                print 'Best results of the moment',fvector,best_result_rem
                if best_result_rem > res_vector[dim-1]:
                    fvector[best_feature_rem]=0
                    dim = dim -1

                    if(best_result < best_result_rem):
                        bestdim = dim
                        best_result = best_result_rem
                        best_fvector = list(fvector)
                        print "Updating best feature vector"
                    res_vector[dim] = best_result_rem
                else:
                    backwards = 0
            else:
                backwards = 0
        print ''
	print 'Best results at end', best_fvector, best_result
        print ''
        dim = dim +1
    print res_vector
    return best_fvector, best_result

featurevector,top_score = ffsearch()
print 'Best features',featurevector
print 'Best score',top_score
selectionvector.write(str(featurevector))
#finaltest = testclassifier

