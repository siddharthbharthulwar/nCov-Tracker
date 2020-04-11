import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime
from matplotlib.figure import Figure
from region import Region
import numpy as np 
from scipy.signal import savgol_filter
from state import State
from datetime import datetime, timedelta
import sys

def datePadding(string):
    if (string[0] == '0'):
        return string[1: ]
    else:
        return string

def predictionDatePadding(string):

    if (string[0] == '0'):
        
        return string[1: ].replace(" ", "")
        
    else:

        return string.replace(" ", "")


class CovidDataset:  
    
    # init method or constructor   
    def __init__(self):  
        self.load()

    def load(self):
        #global data from JHU 
        self.confirmedSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        error_bad_lines=False)
        self.deathsSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
        error_bad_lines=False)

        self.recoveredSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
        error_bad_lines=False)

        #Smaller US Data from JHU is in progress right now
        if self.deathsSeries.columns[-1] == self.confirmedSeries.columns[-1]:

            self.currentDate = self.recoveredSeries.columns[-1]
            self.firstDate = self.recoveredSeries.columns[4]
            
            self.dateTime = pd.date_range(start = self.firstDate, end = self.currentDate, freq ='D')
            self.tempDates = self.dateTime.strftime('%m/%e/%y')

            self.dates = []
            for i in range(len(self.tempDates)):
                self.dates.append(datePadding(self.tempDates[i]).replace(" ", ""))

            self.totalConfirmed = []
            self.totalDeaths = []
            self.totalRecovered = []
            
            for i in range(0, len(self.dates)):

                self.totalConfirmed.append(self.confirmedSeries[self.dates[i]].sum())
                self.totalDeaths.append(self.deathsSeries[self.dates[i]].sum())        
                self.totalRecovered.append(self.recoveredSeries[self.dates[i]].sum())


            self.regions = []            

            for index, row in self.confirmedSeries.iterrows():
                r = row.tolist()
                self.regions.append(Region(r[1], r[0], r[4: len(r)]))

            for index, row in self.deathsSeries.iterrows():
                r = row.tolist()
                self.regions[index].addDeaths(r)

            for index, row in self.recoveredSeries.iterrows():
                r = row.tolist()
                self.regions[index].addRecovered(r)

            finalValues = []

            for region in self.regions:

                finalValues.append(region.rowData[-1])

            self.indices = sorted(range(len(finalValues)), key=lambda k: finalValues[k])
            self.indices.reverse()
            self.highestInTheRoom(12)

        else:

            print("ERROR: DATASETS ARE NOT ALIGNED")
            sys.exit()

    def currentWorldFigure(self):

        plt.style.use('bmh')
        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        ax.plot(self.dateTime, self.totalConfirmed, label = "Total Cases: " + str(self.totalConfirmed[-1]))
        ax.plot(self.dateTime, self.totalDeaths, label = "Total Deaths: " + str(self.totalDeaths[-1]))
        ax.plot(self.dateTime, self.totalRecovered, label = "Total Recovered: " + str(self.totalRecovered[-1]))

        index = 0
        for label in ax.xaxis.get_ticklabels():
            if not index == 0 or not index == len(ax.xaxis.get_ticklabels()) - 1:
                label.set_visible(False)
            index += 1

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():
            plt.setp(text, color = 'black')
        ax.set_title(str(self.totalConfirmed[-1]) + " cases, " + str(self.totalDeaths[-1]) + " deaths, and " + str(self.totalRecovered[-1]) + 
        " recovered cases as of " + self.currentDate, fontsize = 10)
        return fig

    def currentCountriesFigure(self):

        plt.style.use('bmh')
        fig = plt.figure(facecolor= (0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))

        newRegions = []
        countries = []
        last = []

        for i in range(0, len(self.regions)):

            region = self.regions[i]
            newRegions.append(region)
            countries.append(region.countryName)
            last.append(region.rowData[-1])

        newIndices = sorted(range(len(last)), key=lambda k: last[k])
        newIndices.reverse()
        newIndices = newIndices[:12 ]

        for index in newIndices:

            rgn = newRegions[index]
            ax.plot(rgn.numList, rgn.rowData,
            label = rgn.countryName + " with " + str(rgn.rowData[-1]) + " cases on " + self.currentDate)

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():

            plt.setp(text, color = "black")

        ax.set_title("Worldwide Cases of COVID-19")
        return fig

        

    def worldPrediction(self, dayParam):

        days = dayParam - 2

        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))
        plt.style.use('bmh')

        predictions = []
        countries = []
        newRegions = []
        chinaSum = 0
        for i in range(0, len(self.regions)):
            region = self.regions[i]

            if region.rowData[-1] > 50 and not region.countryName == "China":
                
                newRegions.append(region)
                region.exponentialPrediction(days)
                countries.append(region.countryName)
                predictions.append(region.exponentialFinalPopulation)
            
            elif region.countryName == "China":

                chinaSum += region.rowData[-1]

        newIndices = sorted(range(len(predictions)), key=lambda k: predictions[k])
        newIndices.reverse()
        newIndices = newIndices[:12]

        
        for index in newIndices:
            rgn = newRegions[index]
            ax.scatter(rgn.numList, rgn.rowData)
            ax.plot(rgn.lins, rgn.vals,  #TODO: change to actual values
            label = rgn.countryName + " with " + str(rgn.exponentialFinalPopulation) + " cases in " + 
            str(dayParam) + " days")

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():
            plt.setp(text, color = 'black')

        date = self.dateTime[-1] + timedelta(days = dayParam)
        ax.set_title(str(sum(predictions)) + " Cases Worldwide by " + predictionDatePadding(date.strftime('%m/%e/%y')))
        ax.set_xlim(left = 30)
        return fig

    def reportdate(self, days):

        date = self.dateTime[-1] + timedelta(days = days)
        return date.strftime('%m/%e/%y')

    def worldDifferential(self):
        
        plt.style.use('bmh')
        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))

        for region in self.regions:

            if region.rowData[-1] > 15000: 
                filtered = savgol_filter(region.differential, 15, 2)
                ax.plot(region.rowData[1: ], filtered, 
                label = region.countryName)

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():
            plt.setp(text, color = 'black')
        ax.set_title("Logistic Trajectory of COVID-19")
        ax.set_xlabel("Total Cases (log)")
        ax.set_ylabel("New Confirmed Cases (log)")
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlim(left = 1000)
        ax.set_ylim(bottom = 100)
        return fig

    def currentUSFigure(self):

        plt.style.use('bmh')
        fig = plt.figure(facecolor = (0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))

        for region in self.regions:

            if region.countryName == "US":

                USRegion = region
                break
                
        ax.plot(self.dateTime, USRegion.rowData, label = 
        "Total Cases in US: " + str(region.rowData[-1]))
        ax.plot(self.dateTime, USRegion.deaths[4: ], label = 
        "Total Deaths in US: " + str(region.deaths[-1]))
        ax.plot(self.dateTime, USRegion.recovered[4: ], label = 
        "Total Recovered in US: " + str(region.recovered[-1]))

        index = 0
        ax.set_xlabel("Days Since First Case")
        ax.set_ylabel("Number of Confirmed Cases")
        for label in ax.xaxis.get_ticklabels():
            if not index == 0 or not index == len(ax.xaxis.get_ticklabels()) - 1:
                label.set_visible(False)
            index += 1

        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():

            plt.setp(text, color = "black")

        ax.set_title("Total Confirmed Cases, Deaths, and Recoveries in the United States", fontsize = 10)
        return fig       

    def highestInTheRoom(self, num):

        finalCases = []
        for region in self.regions:

            finalCases.append(region.rowData[-1])
        

        self.sortedIndices = sorted(range(len(finalCases)), key=lambda k: finalCases[k])
        self.sortedIndices.reverse()
        self.sortedIndices = self.sortedIndices[:num]
        self.sortedRegions = []
        self.sortedNames = []
        
        for i in self.sortedIndices:

            self.sortedRegions.append(self.regions[i])
            self.sortedNames.append(self.regions[i].countryName)




class USDataset: #US Time Series Data has a different structure

    def __init__(self):
        
        self.load()
    
    def load(self):

        self.confirmedSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv",
        error_bad_lines=False)
        self.deathsSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv",
        error_bad_lines=False)

        start = None
        i = -1
        self.states = []

        self.currentDate = self.confirmedSeries.columns[-1]
        self.firstDate = self.confirmedSeries.columns[11]

        self.dateTime = pd.date_range(start = self.firstDate, end = self.currentDate, freq = 'D')
        self.tempDates = self.dateTime.strftime('%m/%e/%y')

        for index, row in self.confirmedSeries.iterrows():

            name = row['Province_State'].replace(" ", "")

            if name == start:

                self.states[i].addConfirmed(row[11: ].tolist())

            else:

                i += 1
                self.states.append(State(name))
                self.states[i].addConfirmed(row[11: ].tolist())
                start = name.replace(" ", "")

        i = -1

        for index, row in self.deathsSeries.iterrows():

            name = row['Province_State'].replace(" ", "")

            if name == start:

                self.states[i].addDeaths(row[12: ].tolist())

            else:

                i += 1
                self.states[i].addDeaths(row[12: ].tolist())
                start = name.replace(" ", "")

        self.highestInTheRoom(12)
    def differential(self, days):


        plt.style.use('bmh')
        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))

        for state in self.states:

            if state.confirmedTotal[-1] > 5000:

                filtered = savgol_filter(np.diff(state.confirmedTotal), 15,
                2)
                ax.plot(state.confirmedTotal[1: ], filtered,
                label = state.name)
        legend = ax.legend(loc = "upper left")
        for text in legend.get_texts():
            plt.setp(text, color = 'black')
        ax.set_title("Logistic Trajectory: United States")
        ax.set_xlabel("Total Cases (log)")
        ax.set_ylabel("New Confirmed Cases (log)")
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlim(left = 1000)
        ax.set_ylim(bottom = 100)
        return fig



    def prediction(self, days):

        plt.style.use('bmh')
        fig = plt.figure(facecolor=(0.17, 0.17, 0.17))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor((0.3, 0.3, 0.3))

        predictions = []
        states = []
        newStates = []

        for i in range(0, len(self.states)):

            
            state = self.states[i]
            state.exponentialModel()

            if state.rowData[-1] > 50:

                newStates.append(state)
                state.exponentialPrediction(days)
                states.append(state.name)
                predictions.append(state.exponentialFinalPopulation)
        
        newIndices = sorted(range(len(predictions)), key=lambda k: predictions[k])
        newIndices.reverse()
        newIndices = newIndices[:12]

        for index in newIndices:

            rgn = newStates[index]
            ax.scatter(rgn.numList, rgn.rowData)
            ax.plot(rgn.lins, rgn.vals, 
            label = rgn.name + " with " + str(rgn.exponentialFinalPopulation) + " cases in " + str(days) + " days")


        leg = ax.legend(loc = "upper left")
        for text in leg.get_texts():
            plt.setp(text, color = 'black')
        
        date = self.dateTime[-1] + timedelta(days = days)

        ax.set_title(str(sum(predictions)) + " Cases in the United States by " + predictionDatePadding(date.strftime('%m/%e/%y')))
        ax.set_xlim(left = 30)
        ax.set_xlabel("Days Since First Case")
        ax.set_ylabel("Confirmed Cases")
        return fig

    def highestInTheRoom(self, num):

        finalCases = []
        for state in self.states:

            finalCases.append(state.confirmedTotal[-1])

        self.sortedIndices = sorted(range(len(finalCases)), key = lambda k: finalCases[k])
        self.sortedIndices.reverse()
        self.sortedIndices = self.sortedIndices[: num]
        self.sortedStates = []
        self.sortedNames = []

        for i in self.sortedIndices:

            self.sortedStates.append(self.states[i])
            self.sortedNames.append(self.states[i].name)





    