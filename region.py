import numpy as np 
import matplotlib.pyplot as plt 
import sklearn


class Region:  
    
    # init method or constructor   
    def __init__(self, countryName, regionName, rowData):  

        self.countryName = countryName
        if not regionName == 'nan':
            self.regionName = regionName

        self.rawRowData = rowData    
        self.rowData = rowData

        self.sets = []
        numList = range(0, len(self.rowData))
        for i in range(len(self.rowData)):

            self.sets.append((numList[i], self.rowData[i]))

        '''
        plt.scatter(numList, self.rowData)
#        plt.plot(numList, self.coefficient * numList + self.intercept)
        plt.title("LogReg for: " + self.countryName)
        plt.show()
        '''

