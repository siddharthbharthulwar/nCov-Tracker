import numpy as np 
import matplotlib.pyplot as plt 

def logisticDistribution(x, a, b, r):

    return (a * r * b * np.exp(-1 * r * x)) / ((1 + (b * np.exp(-1 * r * x))) ** 2)

y = []
for i in np.linspace(-10, 10, num=500):
    y.append(logisticDistribution(i, 2, 1, 1))

plt.plot(np.linspace(-10, 10, num = 500), y)
plt.show()
    