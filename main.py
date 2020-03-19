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
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.state("zoomed")
        root.configure(bg='white')
        root.columnconfigure(1, weight = 8)
        root.columnconfigure(2, weight = 2)
        root.rowconfigure(1, weight = 8)
       # root.resizable(False, False)
        #icon = tk.PhotoImage(file = 'res/logo.png')
        #basic setup

        dataset = CovidDataset()
        canvas = FigureCanvasTkAgg(dataset.figure(1), root)
        canvas2 = FigureCanvasTkAgg(dataset.prediction(1), root)
        canvas3 = FigureCanvasTkAgg(dataset.figure(1), root)

        canvas4 = FigureCanvasTkAgg(dataset.figure(1), root)

        canvas.draw()
        canvas2.draw()

        canvas.get_tk_widget().grid(column = 1, row = 1)
        canvas._tkcanvas.grid(column = 1, row = 1)

        canvas2.get_tk_widget().grid(column = 1, row = 2)
        canvas2._tkcanvas.grid(column = 1, row = 2)

        
        canvas3.get_tk_widget().grid(column = 2, row = 1)
        canvas3._tkcanvas.grid(column = 2, row = 1)

        
        canvas4.get_tk_widget().grid(column = 2, row = 2)
        canvas4._tkcanvas.grid(column = 2, row = 2)

        caseUpdateDisplay = tk.Label(root, text = "Last Updated: " + dataset.currentDate).grid(column = 2, row = 1)
        totalCaseDisplay = tk.Label(root, text = "Total Cases: " + str(dataset.totalConfirmed[-1])).grid(column = 2, row = 2)
        totalDeathDisplay = tk.Label(root, text = "Total Deaths: " + str(dataset.totalDeaths[-1])).grid(column = 2, row = 3)
        totalRecoveredDisplay = tk.Label(root, text = "Total Recovered: " + str(dataset.totalRecovered[-1])).grid(column = 2, row = 4)

        #mainloop for gui => DO NOT TOUCH
        root.mainloop()

def main():
    interface = Interface()


if __name__ == '__main__':main()      