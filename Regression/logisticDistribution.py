import numpy as np 
import matplotlib.pyplot as plt 

def logisticDistribution(x, a, b, r):

    return (a * r * b * np.exp(-1 * r * x)) / ((1 + (b * np.exp(-1 * r * x))) ** 2)

