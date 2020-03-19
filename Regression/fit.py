import functions
from scipy import optimize


def exponentialFit(xData, yData): #bounds will be hardcoded for now
    popt, pcov = optimize.curve_fit(functions.exponential,
    xData, yData, bounds = ((1e-05, 0, -15), (1, 5e-01, 15)))

    return popt, pcov

def logisticfit(xData, yData):
    popt, pcov = optimize.curve_fit(functions.logistic,
    xData, yData, bounds = ((0, 0, 0), (1000000, 500, 1)))
    
    return popt, pcov

def logisticDistributionFit(xData, yData):
    popt, pcov = optimize.curve_fit(functions.logisticDistribution,
    xData, yData) #TODO: implement bounds based on real world observations

    return popt, pcov