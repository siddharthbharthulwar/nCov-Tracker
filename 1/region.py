import numpy as np 
import matplotlib.pyplot as plt 
import sklearn
import math
from Regression.functions import exponential, logistic, logisticDistribution
from Regression.metrics import r_squared
from scipy import optimize
from scipy import misc
from sklearn.metrics import r2_score

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

        nums = range(0, len(self.rowData))
        numVals = exponential(nums, popt_exponential[0], popt_exponential[1], popt_exponential[2])
        
        self.r_squared_exponential = r2_score(self.rowData, numVals)

    def logisticModel(self):

        popt_logistic, pcov_logistic = optimize.curve_fit(logistic, self.numList,
        self.rowData, bounds = ((0, 0, 0), (1000000, 500, 1)))

        lins = np.linspace(0, len(self.rowData), 100)
        vals = logistic(lins, popt_logistic[0], popt_logistic[1], popt_logistic[2])

        nums = range(0, len(self.rowData))
        numVals = logistic(nums, popt_logistic[0], popt_logistic[1], popt_logistic[2])


        self.r_squared_logistic = r2_score(self.rowData, numVals)
        plt.scatter(self.numList, self.rowData)
        plt.plot(lins, vals)
        if (type(self.regionName) == str):
            plt.title("Log for: " + self.regionName + ", " + self.countryName + " w/ r2 = " + str(self.r_squared_logistic))
        else:
            plt.title("Log for: " + self.countryName + "w/ r2  = " + self.r_squared_logistic)
        plt.show()
        print(popt_logistic)

