import numpy as np 
import matplotlib.pyplot as plt
from scipy import optimize

x_array = np.linspace(1,10,10)
y_array = 2 ** x_array
y_noise = 30*(np.random.ranf(10))
y_array += y_noise

def exponential(x, a, k, b):
    return a*np.exp(x*k) + b
'''
popt_exponential, pcov_exponential = optimize.curve_fit(exponential, x_array, y_array)

perr_exponential = np.sqrt(np.diag(pcov_exponential))

lins = np.linspace(1, 10, 100)
vals = exponential(lins, popt_exponential[0], popt_exponential[1], popt_exponential[2])


plt.scatter(x_array, y_array)
plt.plot(lins, vals)
plt.show()
'''