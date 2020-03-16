import numpy as np
import scipy.optimize as opt 
import matplotlib.pyplot as plt 

def f(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x - d))) + b

