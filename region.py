import numpy as np 
import matplotlib.pyplot as plt 
import sklearn
import math
from Regression.exponential import exponential
from scipy import optimize

class Region:  
    
    # init method or constructor   
    def __init__(self, countryName, regionName, rowData):  

        self.countryName = countryName
        if type(regionName) == str:
            self.regionName = regionName
        else:
            self.regionName = " "

        self.rawRowData = rowData    
        self.rowData = rowData
        self.totalCases = self.rowData[-1]
        self.sets = []
        self.numList = range(0, len(self.rowData))
        for i in range(len(self.rowData)):

            self.sets.append((self.numList[i], self.rowData[i]))

        #MODELS:
        if (self.rowData[len(self.rowData) - 1] > 1):

            #self.exponentialModel()
            self.exponentialPrediction(2)
    def quadraticModel(self):
        quadraticModel = np.polyfit(numList, self.rowData, 2)

        quad1dim = np.poly1d(quadraticModel)
        plt.scatter(numList, self.rowData)
        lin = np.linspace(0, len(self.rowData))
        plt.plot(lin, quad1dim(lin))
        plt.title("Quad for: " + self.countryName)
        plt.show()
    def exponentialModel(self):
        popt_exponential, pcov_exponential = optimize.curve_fit(exponential, self.numList, 
        self.rowData, bounds = ((1e-05, 0, -15), (1, 5e-01, 15)))

        lins = np.linspace(0, len(self.rowData), 100)
        vals = exponential(lins, popt_exponential[0], popt_exponential[1], popt_exponential[2])

        plt.scatter(self.numList, self.rowData)
        plt.plot(lins, vals)
        if (self.regionName == " "):
            plt.title("Exp for: " + self.countryName)

        else:
            plt.title("Exp for: " + self.regionName + ", " + self.countryName)

        plt.show()
        print(popt_exponential)

    def exponentialPrediction(self, days):

        popt_exponential, pcov_exponential = optimize.curve_fit(exponential, self.numList, 
        self.rowData, bounds = ((1e-05, 0, -15), (1, 5e-01, 15)))

        self.lins = np.linspace(0, len(self.rowData) + days, 100)
        self.vals = exponential(self.lins, popt_exponential[0], popt_exponential[1], popt_exponential[2])

        '''
        plt.scatter(self.numList, self.rowData)
        plt.plot(self.lins, self.vals)
        if (self.regionName == " "):
            plt.title("Prediction for " + self.countryName + " after " + str(days) + " days: " + str(int(vals[-1])))

        else:
            plt.title("Prediction for "  + self.regionName + ", " + self.countryName + " after" + str(days) + " days:" + str(int(vals[-1])))
        plt.xlabel("Days Since First Case")
        plt.ylabel("Confirmed Cases")
        plt.show()
        '''


