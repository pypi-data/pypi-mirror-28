import numpy

def zscore(A,axis=0):
    A = numpy.array(A,dtype=float)
    avg = numpy.average(A, axis=axis)
    std = numpy.std(A, axis=axis)
    if not axis:
        for i in range(0,A.shape[1]):
            A[:,i] = (A[:,i] - avg[i]) / std[i];
    else:
        for i in range(0,A.shape[0]):
            A[i,:] = (A[i,:]- avg[i]) / std[i];
    return A

