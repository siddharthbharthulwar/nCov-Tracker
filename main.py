import tkinter as tk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from dataset import CovidDataset

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class Interface:

    def __init__(self):
        
        root = tk.Tk()
        root.title("2019 nCov Tracker")
        root.geometry("700x700")
        root.configure(bg='white')
        root.columnconfigure(1, weight = 8)
        root.columnconfigure(2, weight = 2)
        root.rowconfigure(1, weight = 8)
       # root.resizable(False, False)
        #icon = tk.PhotoImage(file = 'res/logo.png')
        #basic setup

        dataset = CovidDataset()
        for region in dataset.regions:
            if (region.countryName == "China"):

                region.logisticModel()
        
        canvas = FigureCanvasTkAgg(dataset.figure(), root)
        canvas.draw()

        canvas.get_tk_widget().grid(column = 1, row = 1)
        canvas._tkcanvas.grid(column = 1, row = 1)

        caseUpdateDisplay = tk.Label(root, text = "Last Updated: " + dataset.currentDate).grid(column = 2, row = 1)
        totalCaseDisplay = tk.Label(root, text = "Total Cases: " + str(dataset.totalConfirmed[-1])).grid(column = 2, row = 2)
        totalDeathDisplay = tk.Label(root, text = "Total Deaths: " + str(dataset.totalDeaths[-1])).grid(column = 2, row = 3)
        totalRecoveredDisplay = tk.Label(root, text = "Total Recovered: " + str(dataset.totalRecovered[-1])).grid(column = 2, row = 4)

        #mainloop for gui => DO NOT TOUCH
        root.mainloop()

def main():
    interface = Interface()


if __name__ == '__main__':main()      