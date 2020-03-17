import numpy as np 
import matplotlib.pyplot as plt
from scipy import optimize

def exponential(x, a, k, b):
    return a*np.exp(x*k) + b

