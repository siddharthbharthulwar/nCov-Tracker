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

        self.popt_exponential, self.pcov_exponential = 