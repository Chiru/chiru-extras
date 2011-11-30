from numpy import *

def extract(data, wsize, overlap, fs):
    """Function calculates features over a data array in a slinding window
    of size wsize with given overlap. The features calculated are
    determined by a function list fs. 
    """
    total=data.size /(wsize-overlap);
    features = zeros((total, len(fs)));
    k = 0;
    for func in fs:
        for i in range (0, total):
            features[i,k] = func(data[i:(i+wsize-1)])
            i = i +wsize- overlap;
        k = k + 1
    return features


def writeARFFHeader(fname, flabels, clabels):
    """writes the header for an arff file
    """    
    f = open(fname, 'w')
    f.write('@relation testing\n\n')
    n = 0;
    for feat in flabels:
        f.write('@ATTRIBUTE\t'+feat+'\tNUMERIC\n')

    f.write('@ATTRIBUTE\tclass\t{')
    for cls in clabels:
        if (n != size(cls)):
            f.write(cls+',')
        else:
            f.write(cls+'}\n\n')
        n += 1;
    f.write('@DATA\n')
    f.flush()
    f.close()
    
def writeToARFF(fname, features, clabel):
    """writes a feature vector to an arff weka file
    """
    f = open(fname, 'a')
    shape=features.shape
    for n in range(0, shape[0]):
        for m in range(0, shape[1]):
            f.write(''+str(features[n,m])+',')
        f.write(clabel+'\n')
    
