import tkinter as tk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib as mpl
from dataset import CovidDataset, USDataset

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class Interface:

    def __init__(self):

        #INIT CONFIGURATION WINDOW
        self.splash = tk.Tk()
        self.dataset = CovidDataset()
        self.usdataset = USDataset()
        self.splash.title("Configuration Settings")
        self.splash.geometry("300x200")
        self.splash.configure(bg = "grey17")

        choicesDict = {}
        usChoicesDict = {}

        index = 0
        for i in self.dataset.sortedNames:

            choicesDict[i] = self.dataset.sortedRegions[index]
            index +=1
        
        choicesDict['Worldwide'] = None
        tkVar = tk.StringVar(master = self.splash)
        tkVar.set('Worldwide')

        index = 0
        for i in self.usdataset.sortedNames:

            usChoicesDict[i] = self.usdataset.sortedStates[index]
            index +=1
        
        usVar = tk.StringVar(master = self.splash)
        usVar.set('Colorado')

        popupMenu = tk.OptionMenu(self.splash, tkVar, *choicesDict)
        popupMenu.grid(column = 3, row = 2)

        usPopupMenu = tk.OptionMenu(self.splash, usVar, *usChoicesDict)
        usPopupMenu.grid(column = 3 , row = 4)

        execute = tk.Button(self.splash, text = "Enter", command = lambda: self.load())
        execute.grid(column = 3, row = 3)

        self.splash.mainloop()

        #END CONFIGURATION WINDOW

    def load(self):
        self.splash.destroy()

        COLOR = 'white'
        mpl.rcParams['text.color'] = COLOR
        mpl.rcParams['axes.labelcolor'] = COLOR
        mpl.rcParams['xtick.color'] = COLOR
        mpl.rcParams['ytick.color'] = COLOR
        
        self.root = tk.Tk()
       # root.iconphoto(False, tk.PhotoImage(file = 'res/logo.png'))
        self.root.title("2019 nCov Statistical Toolkit")

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.state("zoomed")
        self.root.configure(bg = "grey17")

        self.canvas = FigureCanvasTkAgg(self.dataset.currentWorldFigure(), self.root)
        self.canvas.get_tk_widget().grid(column = 1, row = 1)
        
        self.canvas2 = FigureCanvasTkAgg(self.dataset.worldPrediction(3), self.root)
        self.canvas2.get_tk_widget().grid(column = 1, row = 2)

        self.canvas3 = FigureCanvasTkAgg(self.dataset.worldDifferential(), self.root)
        self.canvas3.get_tk_widget().grid(column = 2, row = 1)

        self.canvas4 = FigureCanvasTkAgg(self.usdataset.prediction(3), self.root)
        self.canvas4.get_tk_widget().grid(column = 2, row = 2)
        
        self.canvas5 = FigureCanvasTkAgg(self.usdataset.differential(5), self.root)
        self.canvas5.get_tk_widget().grid(column = 3, row = 1)

        self.canvas6 = FigureCanvasTkAgg(self.dataset.currentUSFigure(), self.root)
        self.canvas6.get_tk_widget().grid(column = 3, row = 2)
        

        ## show window again
        self.root.mainloop()





def main():

    interface = Interface()

if __name__ == '__main__':

    main()
