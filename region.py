import numpy as np 
import matplotlib.pyplot as plt 
import sklearn
import math
from Regression.functions import exponential, logistic, logisticDistribution
from Regression.metrics import r_squared
from scipy import optimize
from scipy import misc
from sklearn.metrics import r2_score

def square(array):

    ret = []
    for item in array:
        ret.append((item ** 3) + 1)
    return ret

class Region:  
    
    # init method or constructor   
    def __init__(self, countryName, regionName, rowData):  

        self.countryName = countryName
        if type(regionName) == str:
            self.regionName = regionName
        else:
            self.regionName = None

        self.rowData = rowData
        self.totalCases = self.rowData[-1]
        self.numList = range(0, len(self.rowData))

        self.exponentialModel()
        #self.logisticModel()

    def addDeaths(self, deaths):

        self.deaths = deaths

    def addRecovered(self, recovered):

        self.recovered = recovered

    def exponentialModel(self):
        self.popt_exponential, self.pcov_exponential = optimize.curve_fit(exponential, self.numList, 
        self.rowData, bounds = ((1e-05, 0, -15), (1, 5e-01, 15)))

        nums = range(0, len(self.rowData))
        numVals = logistic(nums, self.popt_exponential[0], self.popt_exponential[1], self.popt_exponential[2])

        self.r_squared_exponential = r2_score(self.rowData, numVals)

    def logisticModel(self):

        self.popt_logistic, self.pcov_logistic = optimize.curve_fit(logistic, self.numList,
        self.rowData, bounds = ((0, 0, 0), (1000000, 500, 1)))

        nums = range(0, len(self.rowData))
        numVals = logistic(nums, self.popt_logistic[0], self.popt_logistic[1], self.popt_logistic[2])

        self.r_squared_logistic = r2_score(self.rowData, numVals)

    def exponentialPrediction(self, days):


        self.lins = np.linspace(0, len(self.rowData) + days, 100)

        self.vals = exponential(self.lins, self.popt_exponential[0], 
        self.popt_exponential[1], self.popt_exponential[2])

        if (self.countryName == 'Burma'):
            print('ACTIVATED')
        self.exponentialFinalPopulation = int(self.vals[-1])

    def logisticPrediction(self, days):

        self.lins = np.linspace(0, len(self.rowData) + days, 100)

        self.vals = logistic(self.lins, self.logisticModel[0], 
        self.logisticModel[1], self.logisticModel[2])

        self.logisticFinalPopulation = int(self.vals[-1])


