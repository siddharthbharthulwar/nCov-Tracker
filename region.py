import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
import sklearn
import math
from Regression.functions import exponential, logistic, logisticDistribution
from Regression.metrics import r_squared
from scipy import optimize
from scipy import misc
from scipy.signal import savgol_filter
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
        self.differential = np.diff(self.rowData)

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

    
    def regionPredictionPlot(self, days, date):

        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')

        self.exponentialPrediction(days)
        ax.scatter(self.numList, self.rowData)
        ax.plot(self.lins, self.vals, label = self.countryName + " with " + str(self.exponentialFinalPopulation) + " cases in " + str(days) + " days")

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():
            plt.setp(text, color = "black")

        ax.set_title(str(self.exponentialFinalPopulation) + " Cases in " + self.countryName + " by " + date)
        ax.set_xlim(left = 30)
        return fig

    def regionDifferentialPlot(self):

        fig = plt.figure(facecolor = (0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')
        filtered = savgol_filter(self.differential, 15, 2)
        ax.plot(self.rowData[1: ], filtered, label = self.countryName)

        legend = ax.legend(loc = "upper left")
        for text in legend.get_texts():
            plt.setp(text, color = 'black')

        ax.set_title('Logistic Trajectory of ' + self.countryName)
        ax.set_xlabel("Total Cases (log)")
        ax.set_ylabel("New Confirmed Cases (log)")
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlim(left = 1000)
        ax.set_ylim(bottom = 100)
        return fig

    def regionCurrentPlot(self):

        fig = plt.figure(facecolor = (0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')
        
        ax.plot(self.numList, self.rowData, label = "Cases")
        ax.plot(self.numList, self.deaths[4: ], label = "Deaths")
        ax.plot(self.numList, self.recovered[4: ], label = "Recovered")

        ax.set_title("Current Cases, Deaths, and Recoveries in " + self.countryName)
        ax.set_xlabel("Days Since First Case")
        ax.set_ylabel("People in Country")

        ax.set_xlim(left = 30)
        return fig


