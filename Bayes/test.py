import numpy as np
import csv
import itertools
import math
import matplotlib.pyplot as plt
alpha = 0.005
beta = 11.1
M = 5
N = 10
##################loadCsv######################
def loadCsv(filename):
    lines = csv.reader(open(filename, "rb"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset
#################load data from csv file#############
filename = 'aapl1.csv'
dataset = loadCsv(filename)
print ('load data file {0} with {1} rows').format(filename,len(dataset))
dataset.reverse()
dataset = list(itertools.chain(*dataset))
actual_price = dataset[10:11]
print actual_price
print 'The actual price is '+ repr(actual_price[0])
dataset = dataset[0:10]

##################load data from csv file#############
# filename = 'data5.csv'
# dataset = loadCsv(filename)
# print ('load data file {0} with {1} rows').format(filename,len(dataset))
# dataset = list(itertools.chain(*dataset))

################## Train data######################
# X = np.array([[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0]])
# X = np.array([1,2,3,4,5,6,7,8,9,10])
Y = np.array(dataset).reshape(10,1)
# print X
print 'The trend is '
print Y

################## try to output image, not implmented yet #######
# np.random.normal(Y.mean(), Y.std())
#
# mu, sigma = 0, 0.1 # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)
# #print s
#
# count, bins, ignored = plt.hist(s, 30, normed=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#          linewidth=2, color='r')
# plt.show()

##################### get phi x# #################
def getfy(x):
    fy=[]
    for i in range(M+1):
        fy.append(math.pow(x, i))
    fy = np.array(fy)
    fy = fy.reshape(fy.size, 1)
    return fy
# print getfy(11)
# print getfy(M).shape

################# get inverseS#####################
def getInverseS():
    I = np.eye((M+1))
    temp = np.zeros([M+1, 1])
    fy2 = getfy(N+1)
    for i in range(1, N+1):
        fy = getfy(i)
        
        # temp = temp + fy
        temp = temp + fy.dot(fy2.T)
    # inverseS = alpha*I + beta*(temp).dot(fy2.T)
    #######same result!!!!!!!!!!!!!
    inverseS = alpha*I + beta*(temp)
    # print inverseS
    return inverseS

############## get S^2, cunrrently useless##############
# def getInverseS2(x):
#     fy = getfy(x)
#     inverseS = getInverseS()
#     inverseS2 = beta**-1 + fy.T.dot(inverseS).T.dot(fy).dot(Y)
#     return inverseS2

################# get m(x) ############################## 
def getm(x):
    temp = np.zeros([M+1, 1])
    for i in  range(1, N+1):
        fy = getfy(i)
        # print fy
        # print Y[i-1]
        temp =fy*Y[i-1] + temp
        # print temp
    fy2 = getfy(x)
    # print temp
    # print fy2
    S = np.linalg.inv(getInverseS())
    # print S
    m = beta*fy2.T.dot(S).dot(temp)
    return m

predicted_price = getm(11)[0][0]
print 'the predicted price is %f' % predicted_price

print 'the absolute mean error is %f' % abs(predicted_price - actual_price[0])
print 'the relative error is %f' % (abs(predicted_price - actual_price[0])/float(actual_price[0]))







