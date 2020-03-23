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
        #The data is aggregated from the John's Hopkins CSSE, which is updated daily
        self.confirmedSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
        error_bad_lines=False)
        self.deathsSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
        error_bad_lines=False)

        self.recoveredSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv",
        error_bad_lines=False)

        if self.recoveredSeries.columns[-1] == self.deathsSeries.columns[-1] == self.confirmedSeries.columns[-1]:

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

        else:

            print("ERROR: DATASETS ARE NOT ALIGNED")

    def currentWorldFigure(self):

        plt.style.use('ggplot')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self.dateTime, self.totalConfirmed, label = "Total Cases: " + str(self.totalConfirmed[-1]))
        ax.plot(self.dateTime, self.totalDeaths, label = "Total Deaths: " + str(self.totalDeaths[-1]))
        ax.plot(self.dateTime, self.totalRecovered, label = "Total Recovered: " + str(self.totalRecovered[-1]))

        for label in ax.xaxis.get_ticklabels():
            #TODO: actually fix this part
            label.set_visible(False)
            '''
            day = datetime.strptime(label.get_text(), '%m/%e/%y').day
            if not day == 1:
                label.set_visible(False)
            '''
        ax.legend(loc = "upper left")
        ax.set_title(str(self.totalConfirmed[-1]) + " cases, " + str(self.totalDeaths[-1]) + " deaths, and " + str(self.totalRecovered[-1]) + 
        " recovered cases as of " + self.currentDate, fontsize = 10)
        return fig

    def worldPredictions(self, days):

        plt.style.use('ggplot')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        predictions = []

        for region in self.regions:

            region.exponentialPrediction(5)
            predictions.append(region.exponentialFinalPopulation)
        

        top_idx = np.argsort(predictions)[-12:]
        
        for i in range(0, len(self.regions)):

            if i in top_idx:
                print("not finished yet")

    def USPrediction(self, days):

        plt.style.use("ggplot")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        predictions = []
        indices = []
        index = 0
        for region in self.regions:
            region.exponentialPrediction(days)
            predictions.append(region.exponentialFinalPopulation)
            indices.append(index)
            index += 1

        top_idx = np.argsort(predictions)
        usSum = 0
        numUsed = 0
        lins = np.linspace(0, len(self.regions[0].rowData) + days, 100) #TODO: set to non-hardcoded value (not 100)
        for i in range(0, len(top_idx)):

            if self.regions[i].countryName == 'US' and numUsed < 13:

                region = self.regions[i]
                
                ax.scatter(region.numList, region.rowData)
                ax.plot(lins, region.vals, label = region.regionName + " with " 
                    + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " days r2 = " 
                    + str(round(region.r_squared_exponential, 3)))
                usSum += int(region.vals[len(region.vals) - 1])

        ax.legend(loc="upper left")
        ax.set_title("Cases Within the United States: " + str(usSum))
        return fig
                

            
        
    #def refresh(self, days):

