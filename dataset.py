import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime
from matplotlib.figure import Figure


def datePadding(string):
    if (string[0] == '0'):
        return string[1: ]
    else:
        return string


class CovidDataset:  
    
    # init method or constructor   
    def __init__(self):  


        self.confirmedSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
        error_bad_lines=False)

        self.deathsSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
        error_bad_lines=False)

        self.recoveredSeries = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv",
        error_bad_lines=False)

        if self.recoveredSeries.columns[-1] == self.deathsSeries.columns[-1] == self.confirmedSeries.columns[-1]:

            self.currentDate = self.recoveredSeries.columns[-1]
            self.firstDate = self.recoveredSeries.columns[4]
            

            self.dateTime = pd.date_range(start = self.firstDate, end = self.currentDate, freq ='D')#.datetime.strftime('%M/%D/%Y')
            tempDates = self.dateTime.strftime('%m/%e/%y')

            self.dates = []
            for i in range(len(tempDates)):
                self.dates.append(datePadding(tempDates[i]).replace(" ", ""))

            self.totalConfirmed = []
            self.totalDeaths = []
            self.totalRecovered = []
            
            for i in range(len(self.dates)):

                self.totalConfirmed.append(self.confirmedSeries[self.dates[i]].sum())
                self.totalDeaths.append(self.deathsSeries[self.dates[i]].sum())        
                self.totalRecovered.append(self.recoveredSeries[self.dates[i]].sum())
                
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

        fig = Figure()
        fig.plo

cov = CovidDataset()
