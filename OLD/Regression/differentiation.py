import numpy as np
import matplotlib.pyplot as plt 

x = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
z = [0, 1, 2, 3, 4, 5, 6, 7]

print(len(y), "y")
print(len(x), "x")

def derivative(array): #assumes time discretization of data is constant 
    ret = []
    for i in range(0, len(array) - 2):
        ret.append(array[i + 1] - array[i])
    return ret

der = derivative(x)


plt.scatter(y, x)
plt.plot(z, derivative(x))
plt.show()