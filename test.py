import numpy as np 

predictions = [1, 7, 4, 345 ,7, 2334, 7, 86, 765, 23, 36 ,675, 6435 ,325 ,34, 356 ,345, 3543, 5435 ,435,43, 53, ]
x = sorted(range(len(predictions)), key=lambda k: predictions[k])
x.reverse()
print(x[: 3])