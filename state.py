import numpy as np
from Regression.functions import exponential, logistic, logisticDistribution
from scipy import optimize
from scipy import misc 
from sklearn.metrics import r2_score


class State: #US Time Series Data has a different structure

    def __init__(self, name):
        
        self.name = name
        self.confirmedRows = []
        self.deathsRows = []

    def addConfirmed(self, row):

        self.confirmedRows.append(row)

    def addDeaths(self, row):

        self.deathsRows.append(row)
        self.sum()

    def sum(self):

        self.confirmedTotal = np.sum(np.array(self.confirmedRows), 0)
        self.deathstotal = np.sum(np.array(self.deathsRows), 0)


    def exponentialModel(self):
        self.numList = range(0, len(self.confirmedTotal))
        self.rowData = self.confirmedTotal
        self.popt_exponential, self.pcov_exponential = optimize.curve_fit(exponential, self.numList, 
        self.rowData, bounds = ((1e-05, 0, -15), (1, 5e-01, 15)))

        nums = range(0, len(self.rowData))
        numVals = logistic(nums, self.popt_exponential[0], self.popt_exponential[1], self.popt_exponential[2])

        self.r_squared_exponential = r2_score(self.rowData, numVals)

    def exponentialPrediction(self, days):

        self.lins = np.linspace(0, len(self.rowData) + days, 100)
        self.vals = exponential(self.lins, self.popt_exponential[0],
        self.popt_exponential[1], self.popt_exponential[2])

        self.exponentialFinalPopulation = int(self.vals[-1])


    