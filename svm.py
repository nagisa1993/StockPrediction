import numpy as np
import fetchdata
from sklearn.svm import SVR


def svm_predict(name='YHOO'):
    N = 10
    # Generate sample data
    X = np.arange(N).reshape(N, 1)
    y = fetchdata.get_data(name).ravel()
    # print y

    # Fit regression model
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_lin = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    y_rbf = svr_rbf.fit(X, y).predict(N+1)
    y_lin = svr_lin.fit(X, y).predict(N+1)
    y_poly = svr_poly.fit(X, y).predict(N+1)
    # print y_rbf
    # print y_lin
    # print y_poly
    return y_lin

if __name__=='__main__':
    print svm_predict('AAPL')