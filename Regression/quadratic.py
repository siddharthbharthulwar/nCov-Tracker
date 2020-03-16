import numpy as np 
import matplotlib.pyplot as plt 


x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 9, 15, 22])

z = np.polyfit(x, y, 2)
p = np.poly1d(z)

lin = np.linspace(0, 5, num=50)
plt.scatter(x, y)
plt.plot(lin, p(lin))
plt.show()