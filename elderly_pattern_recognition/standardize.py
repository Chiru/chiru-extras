import numpy as np
#import csv
import pandas as pd

#dataset = csv.reader(open('datatest.csv', 'rb'), delimiter=',')

dataset = pd.read_csv('datatest.csv', index_col=0, parse_dates=True)
locations = pd.read_csv('locations.csv', index_col=0, parse_dates=True)
print len(dataset)
print len(locations)

standardized = {}

for column in dataset:
    #print len(dataset[column])
    st = []
    if column == 'Time':
        continue
    if column == 'Annotations':
        continue
    for f in dataset[column]:
        #print '****'
        #print f
        f = f-np.mean(dataset[column])
        #print f
        f = f/np.std(dataset[column])
        #print f
        #print '****'
        st.append(f)
    standardized[column]=st

# index = dataset.index
# print index
# print '******************'
# arindex = np.array(index)
# print arindex
# print '******************'
# np.random.shuffle(arindex)
# print arindex
# print '******************'

stset = pd.DataFrame(standardized)
#stset['Locations']=locations
storder = stset.dropna()
storder.to_csv('dataorder.csv')
#print stset
newindex=range(len(stset.index))
anno = dataset['Annotations']
anno.index=newindex
locations.index = newindex
#print newindex
shindex = np.random.shuffle(newindex)
#print newindex
#stset.index = dataset.index
stset['Annotations']=anno
stset['Locations']=locations
stset = stset.reindex(newindex)
#print stset

#Want to replace or drop NaN?
stset = stset.dropna()

#print stset

stset.to_csv('datatestst.csv')
