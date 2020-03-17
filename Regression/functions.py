import numpy as np 

def logistic(x, a, b, r):

    return a / (1 + (b * np.exp(-1 * r * x)))

def exponential(x, a, k, b):
    return a*np.exp(x*k) + b

def logisticDistribution(x, a, b, r):

    return (a * r * b * np.exp(-1 * r * x)) / ((1 + (b * np.exp(-1 * r * x))) ** 2)

