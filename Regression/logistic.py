import numpy as np 
import matplotlib.pyplot as plt

def logistic(x, a, b, r):

    return a / (1 + (b * np.exp(-1 * r * x)))
