import numpy as np 
import matplotlib.pyplot as plt

def logistic(x, a, b, r):

    return a / (1 + (b * np.exp(-1 * r * x)))


y = []
for i in np.linspace(-10, 10, num=500):
    y.append(logistic(i, 2, 1, 1))

plt.plot(np.linspace(-10, 10, num = 500), y)
plt.show()