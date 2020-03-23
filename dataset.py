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

    def figure(self, days):

        plt.style.use("ggplot")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self.dateTime, self.totalConfirmed, label = "Total Cases")
        ax.plot(self.dateTime, self.totalDeaths, label = "Total Deaths")
        ax.plot(self.dateTime, self.totalRecovered, label = "Total Recovered")

        
        for label in ax.xaxis.get_ticklabels()[::1]:
            label.set_visible(False)

        ax.legend(loc="upper left")
        ax.set_title(str(self.totalConfirmed[-1]) + " cases, " + str(self.totalDeaths[-1]) + " deaths, and " + str(self.totalRecovered[-1]) + 
        " recovered cases as of " + self.currentDate, fontsize = 12)
        return fig
    
    def USPrediction(self, days):

        plt.style.use("ggplot")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        USSum = 0
        for i in range(0, len(self.regions)):
            region = self.regions[i]

            if (region.totalCases > 300 and  region.countryName == "US"): #excluding china due to anomalous regression

                region.exponentialPrediction(days - 1)
                if (region.r_squared_exponential > 0.9):
                    ax.scatter(region.numList, region.rowData)
                    ax.plot(region.lins, region.vals, label = region.regionName + " with " 
                        + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " days r2 = " 
                        + str(round(region.r_squared_exponential, 3)))
                    print(region.regionName + " with " 
                        + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " days")
                    USSum += int(region.vals[len(region.vals) - 1])
        ax.legend(loc="upper left")
        ax.set_title("Cases Within the United States", fontsize = 12)
        return fig

    def WorldPrediction(self, days):

        plt.style.use('ggplot')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        US = 0
        China = 0
        Canada = 0
        Australia = 0


        for i in range(0, len(self.regions)):

            region = self.regions[i]

            if (region.totalCases > 300):

                if (type(region[0]) == str):

                    if (region[1] == 'US'):

                        US += region.vals[len(region.vals) - 1]

                    elif (region[1] == 'China'):

                        China += region.vals[len(region.vals) - 1]

                    elif (region[1] == 'Canada'):

                        Canada += region.vals[len(region.vals) - 1]

                    elif (region[1] == 'Australia'):

                        Australia += region.vals[len(region.vals) - 1]

                else:

                    ax.scatter(region.numList, region.rowData)
                    if days == 0:

                        ax.plot(region.lins, region.vals, label = region.countryName + " w/ " 
                            + str(int(region.vals[len(region.vals) - 1])) + " cases today, r2 = " 
                            + str(round(region.r_squared_exponential, 3)))              
                    elif days == 1:

                        ax.plot(region.lins, region.vals, label = region.countryName + " w/ " 
                            + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " day,r2 = " 
                            + str(round(region.r_squared_exponential, 3)))
                    else:

                        ax.plot(region.lins, region.vals, label = region.countryName + " w/ " 
                            + str(int(region.vals[len(region.vals) - 1])) + " cases in " + str(days) + " days r2 = " 
                            + str(round(region.r_squared_exponential, 3)))

    