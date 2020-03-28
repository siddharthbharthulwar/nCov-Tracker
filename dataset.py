import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime
from matplotlib.figure import Figure
from region import Region
import numpy as np 


def datePadding(string):
    if (string[0] == '0'):
        return string[1: ]
    else:
        return string

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
            
            self.confirmedSeries.sort_values(by=self.currentDate, ascending=False)
            print(self.confirmedSeries)
            self.dateTime = pd.date_range(start = self.firstDate, end = self.currentDate, freq ='D')
            tempDates = self.dateTime.strftime('%m/%e/%y')

            self.dates = []
            for i in range(len(tempDates)):
                self.dates.append(datePadding(tempDates[i]).replace(" ", ""))

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

        else:

            print("ERROR: DATASETS ARE NOT ALIGNED")

    def currentWorldFigure(self):

        plt.style.use('ggplot')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self.dateTime, self.totalConfirmed, label = "Total Cases: " + str(self.totalConfirmed[-1]))
        ax.plot(self.dateTime, self.totalDeaths, label = "Total Deaths: " + str(self.totalDeaths[-1]))
        ax.plot(self.dateTime, self.totalRecovered, label = "Total Recovered: " + str(self.totalRecovered[-1]))

        index = 0
        for label in ax.xaxis.get_ticklabels():
            if not index == 0 or not index == len(ax.xaxis.get_ticklabels()) - 1:
                label.set_visible(False)
            index += 1

        ax.legend(loc = "upper left")
        ax.set_title(str(self.totalConfirmed[-1]) + " cases, " + str(self.totalDeaths[-1]) + " deaths, and " + str(self.totalRecovered[-1]) + 
        " recovered cases as of " + self.currentDate, fontsize = 10)
        return fig

    def worldPrediction(self, days):

        plt.style.use('ggplot')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

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
            str(days) + " days")

        ax.legend(loc = "upper left")
        ax.set_title(str(sum(predictions) + chinaSum) + " Cases Worldwide in " + str(days) + " Days")
        
        return fig
        