import numpy as np 
import matplotlib.pyplot as plt 
import sklearn
from Regression.exponential import exponential
from scipy import optimize

class Region:  
    
    # init method or constructor   
    def __init__(self, countryName, regionName, rowData):  

        self.countryName = countryName
        if not regionName == 'nan':
            self.regionName = regionName

        self.rawRowData = rowData    
        self.rowData = rowData

        self.sets = []
        self.numList = range(0, len(self.rowData))
        for i in range(len(self.rowData)):

            self.sets.append((self.numList[i], self.rowData[i]))

        #MODELS:
        self.exponentialModel()
    def quadraticModel(self):
        quadraticModel = np.polyfit(numList, self.rowData, 2)

        quad1dim = np.poly1d(quadraticModel)
        plt.scatter(numList, self.rowData)
        lin = np.linspace(0, len(self.rowData))
        plt.plot(lin, quad1dim(lin))
        plt.title("Quad for: " + self.countryName)
        plt.show()
    def exponentialModel(self):
        popt_exponential, pcov_exponential = optimize.curve_fit(exponential, self.numList, self.rowData)

        lins = np.linspace(0, len(self.rowData), 100)
        vals = exponential(lins, popt_exponential[0], popt_exponential[1], popt_exponential[2])

        plt.scatter(self.numList, self.rowData)
        plt.plot(lins, vals)
        plt.title("Exp for: " + self.countryName)
        plt.show()


