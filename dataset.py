import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime
from matplotlib.figure import Figure
from region import Region

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
            #print(self.confirmedSeries.loc[0:1, 1])
            

            for index, row in self.confirmedSeries.iterrows():
                r = row.tolist()
                self.regions.append(Region(r[1], r[0], r[4: len(r)]))
                
        else:

            print("ERROR: DATASETS ARE NOT ALIGNED")

    def plot(self):

        plt.style.use('ggplot')
        plt.plot(self.dateTime, self.totalConfirmed, label = "Total Cases")
        plt.plot(self.dateTime, self.totalDeaths, label = "Total Deaths")
        plt.plot(self.dateTime, self.totalRecovered, label = "Total Recovered")

        title = "Worldwide 2019 nCov Coverage as of " + self.currentDate
        plt.title(title)
        plt.legend(loc="lower right")

        plt.ylabel("Cases")
        plt.xlabel("Date")
        plt.show()

    def figure(self):

        plt.style.use("ggplot")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self.dateTime, self.totalConfirmed, label = "Total Cases")
        ax.plot(self.dateTime, self.totalDeaths, label = "Total Deaths")
        ax.plot(self.dateTime, self.totalRecovered, label = "Total Recovered")
        '''
        for i in range(0, len(ax.xaxis.get_ticklabels()) - 1):
            ax.xaxis.get_ticklabels()[i].set_visible(False)
        '''
        
        for label in ax.xaxis.get_ticklabels()[::1]:
            label.set_visible(False)

        ax.legend(loc="upper left")
        return fig
    
    def prediction(self, days):

        plt.style.use("ggplot")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for i in range(0, len(self.regions)):
            region = self.regions[i]

            if (region.totalCases > 50 and region.countryName == "US"): #excluding china due to anomalous regression

                region.exponentialPrediction(days)
                ax.scatter(region.numList, region.rowData)
                ax.plot(region.lins, region.vals, label = region.regionName + " with " 
                    + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " days")
                print(region.regionName + " with " 
                    + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " days")
        ax.legend(loc="upper left")
        plt.show()

    