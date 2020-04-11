import numpy as np
from Regression.functions import exponential, logistic, logisticDistribution
from scipy import optimize
from scipy import misc 
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from sklearn.metrics import r2_score
from scipy.signal import savgol_filter


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


    def stateCurrentPlot(self):

        fig = plt.figure(facecolor = (0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')
        
        ax.plot(self.numList, self.confirmedTotal, label = "Cases")
        ax.plot(self.numList, self.deathstotal, label = "Deaths")

        ax.set_title("Current Cases, Deaths, and Recoveries in " + self.name)
        ax.set_xlabel("Days Since First Case")
        ax.set_ylabel("People in State")

        ax.set_xlim(left = 30)
        return fig

    def statePredictionPlot(self, days, date):


        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')

        self.exponentialPrediction(days)
        ax.scatter(self.numList, self.rowData)
        ax.plot(self.lins, self.vals, label = self.name + " with " + str(self.exponentialFinalPopulation) + " cases in " + str(days) + " days")

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():
            plt.setp(text, color = "black")

        ax.set_title(str(self.exponentialFinalPopulation) + " Cases in " + self.name + " by " + date)
        ax.set_xlim(left = 30)
        return fig

    def stateDifferentialPlot(self):
        
        self.differential = np.diff(self.confirmedTotal)
        fig = plt.figure(facecolor = (0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')
        filtered = savgol_filter(self.differential, 15, 2)
        ax.plot(self.confirmedTotal[1: ], filtered, label = self.name)

        legend = ax.legend(loc = "upper left")
        for text in legend.get_texts():
            plt.setp(text, color = 'black')

        ax.set_title('Logistic Trajectory of ' + self.name)
        ax.set_xlabel("Total Cases (log)")
        ax.set_ylabel("New Confirmed Cases (log)")
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlim(left = 1000)
        ax.set_ylim(bottom = 100)
        return fig




    