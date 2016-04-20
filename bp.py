import numpy as np
 
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
 
    return 1/(1+np.exp(-x))
 
X = np.array([[0,0],
              [0,1],
              [1,0],
              [1,1]])
 
y = np.array([[0],
              [1],
              [1],
              [0]])

# input the target error and learning rate
print "Please enter the target error and learning rate"
e = input()
alpha = input()

 
np.random.seed(10)
 
# randomly initialize our weights with mean 0
syn0 = 2*np.random.random((2,2)) - 1
syn1 = 2*np.random.random((2,1)) - 1
# print type(syn0)
# print syn0.shape

print "The initial weights for first layer:"
print syn0
print "The initial weights for second layer:"
print syn1

count = 0 
# for j in xrange(60000):
while True:
    count = count + 1 

    # Feed forward through layers 0, 1, and 2
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))
    # how much did we miss the target value?
    l2_error = y - l2
   

    if (count% 10000) == 0:
        # print "Error:" + str(np.mean(np.abs(l2_error)))
        print count
        # print "Error:" + str(np.mean(np.abs(l2_error*nonlin(l2,deriv=True))))
        print "Error:" + str(np.mean(np.abs(l2_error*l2_error)))

 
    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = alpha*l2_error*nonlin(l2,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)
 
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = alpha*l1_error * nonlin(l1,deriv=True)
 
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

    if count == 1:
        print "The first-batch error is"
        print str(np.mean(np.abs(l2_error*nonlin(l2,deriv=True))))

    # if (e>=np.mean(np.abs(nonlin(l2,deriv=True)*l2_error))):
    #     break
    # use square or root?
    if (e>=0.5*np.mean(np.abs(l2_error*l2_error))):
        break

print "The final weights for first layer:"
print syn0
print "The final weights for second layer:"
print syn1
print "The final error is " + str(0.5*np.mean(np.abs(l2_error*l2_error)))
print "Totally runs %s batches" %count
