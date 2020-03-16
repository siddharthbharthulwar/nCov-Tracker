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

        #MODELS:

        quadraticModel = np.polyfit(numList, self.rowData, 2)
        polynomialmodel = np.polyfit(numList, self.rowData, 10)

        quad1dim = np.poly1d(quadraticModel)
        poly1dim = np.poly1d(polynomialmodel)
        plt.scatter(numList, self.rowData)
        lin = np.linspace(0, len(self.rowData))
        plt.plot(lin, quad1dim(lin))
        plt.title("Quad for: " + self.countryName)
        plt.show()
        #END MODELS
        '''
        plt.scatter(numList, self.rowData)
#        plt.plot(numList, self.coefficient * numList + self.intercept)
        plt.title("LogReg for: " + self.countryName)
        plt.show()
        '''

