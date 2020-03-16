import numpy as np 
import matplotlib.pyplot as plt 

from sklearn import linear_model
from scipy.special import expit 

def logisticFit(x, y):
    clf = linear_model.LogisticRegression()
    clf.fit(x, y)

    return clf.coef_, clf.intercept_