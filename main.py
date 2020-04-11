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
        self.tkVar = tk.StringVar(master = self.splash)
        self.tkVar.set('Worldwide')

        index = 0
        for i in self.usdataset.sortedNames:

            usChoicesDict[i] = self.usdataset.sortedStates[index]
            index +=1
        
        self.usVar = tk.StringVar(master = self.splash)
        self.usVar.set('N/A')

        countriesLabel = tk.Label(self.splash, text = "Choose a Country: ", bg = "grey17", fg = "gray97").grid(column = 0, row = 0)

        stateLabel = tk.Label(self.splash, text = "Choose a State (if US is selected): ", bg = "grey17", fg = "gray97").grid(column = 0, row = 1)

        daysLabel = tk.Label(self.splash, text = "Days for Prediction: ", bg = "grey17", fg = "gray97").grid(column = 0, row = 2)

        finalLabel = tk.Label(self.splash, text = "Submit Query: ", bg = "grey17", fg = "gray97").grid(column = 0, row = 3)


        popupMenu = tk.OptionMenu(self.splash, self.tkVar, *choicesDict)
        popupMenu.config(bg = "grey17", fg = "gray97", bd = 0, activebackground = "grey30", highlightthickness = 0)
        popupMenu.grid(column = 3, row = 0)

        usPopupMenu = tk.OptionMenu(self.splash, self.usVar, *usChoicesDict)
        usPopupMenu.config(bg = "grey17", fg = "gray97", bd = 0, activebackground = "grey30", highlightthickness = 0)
        usPopupMenu.grid(column = 3 , row = 1)

        self.daysVar = tk.StringVar(master = self.splash)
        daysField = tk.Entry(self.splash, textvariable = self.daysVar, bg = "grey30", fg = "gray97", bd = 0)
        daysField.grid(column = 3, row = 2)

        execute = tk.Button(self.splash, text = "Enter", command = lambda: self.load())
        execute.grid(column = 3, row = 3)        

        self.splash.mainloop()

    def load(self):
        self.predictionDays = int(self.daysVar.get())
        self.splash.destroy()

        COLOR = 'white'
        mpl.rcParams['text.color'] = COLOR
        mpl.rcParams['axes.labelcolor'] = COLOR
        mpl.rcParams['xtick.color'] = COLOR
        mpl.rcParams['ytick.color'] = COLOR
         
        self.root = tk.Tk()
       # root.iconphoto(False, tk.PhotoImage(file = 'res/logo.png'))
        self.root.title("2019 nCov Statistical Toolkit")

        #w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        #self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.geometry("1300x950")
        #self.root.state("zoomed")
        self.root.configure(bg = "grey17")

        if self.tkVar.get() == 'US':

            self.canvas = FigureCanvasTkAgg(self.dataset.currentUSFigure(), self.root)
            self.canvas.get_tk_widget().grid(column = 1, row = 1)

            self.currentState = None

            for state in self.usdataset.states:

                if state.name == self.usVar.get():

                    self.currentState = state
                    break

            state.exponentialModel()

            self.canvas2 = FigureCanvasTkAgg(state.stateCurrentPlot(), self.root)
            self.canvas2.get_tk_widget().grid(column = 1, row = 2)

            self.canvas3 = FigureCanvasTkAgg(state.statePredictionPlot(self.predictionDays, self.dataset.reportdate(self.predictionDays)))
            self.canvas3.get_tk_widget().grid(column = 2, row = 1)

            self.canvas4 = FigureCanvasTkAgg(state.stateDifferentialPlot(), self.root)
            self.canvas4.get_tk_widget().grid(column = 2, row = 2)

        elif self.tkVar.get() == 'Worldwide':

            self.canvas = FigureCanvasTkAgg(self.dataset.currentWorldFigure(), self.root)
            self.canvas.get_tk_widget().grid(column = 1, row = 1)

            self.canvas2 = FigureCanvasTkAgg(self.dataset.worldPrediction(self.predictionDays), self.root)
            self.canvas2.get_tk_widget().grid(column = 1, row = 2)

            self.canvas3 = FigureCanvasTkAgg(self.dataset.worldDifferential(), self.root)
            self.canvas3.get_tk_widget().grid(column = 2, row = 1)

        else:

            self.canvas = FigureCanvasTkAgg(self.dataset.currentWorldFigure(), self.root)
            self.canvas.get_tk_widget().grid(column = 1, row = 1)

            self.currentRegion = None

            for region in self.dataset.regions:

                if region.countryName == self.tkVar.get():

                    self.currentRegion = region
                    break
            
            self.canvas2 = FigureCanvasTkAgg(region.regionPredictionPlot(self.predictionDays, self.dataset.reportdate(self.predictionDays)))
            self.canvas2.get_tk_widget().grid(column = 1, row = 2)

            self.canvas3 = FigureCanvasTkAgg(region.regionDifferentialPlot(), self.root)
            self.canvas3.get_tk_widget().grid(column = 2, row = 2)

            self.canvas4 = FigureCanvasTkAgg(region.regionCurrentPlot(), self.root)
            self.canvas4.get_tk_widget().grid(column = 2, row = 1)

            
        '''
        self.canvas = FigureCanvasTkAgg(self.dataset.currentWorldFigure(), self.root)
        self.canvas.get_tk_widget().grid(column = 1, row = 1)
        
        self.canvas2 = FigureCanvasTkAgg(self.dataset.worldPrediction(self.predictionDays), self.root)
        self.canvas2.get_tk_widget().grid(column = 1, row = 2)

        self.canvas3 = FigureCanvasTkAgg(self.dataset.worldDifferential(), self.root)
        self.canvas3.get_tk_widget().grid(column = 2, row = 1)

        self.canvas4 = FigureCanvasTkAgg(self.usdataset.prediction(self.predictionDays), self.root)
        self.canvas4.get_tk_widget().grid(column = 2, row = 2)
        
        self.canvas5 = FigureCanvasTkAgg(self.usdataset.differential(self.predictionDays), self.root)
        self.canvas5.get_tk_widget().grid(column = 3, row = 1)

        self.canvas6 = FigureCanvasTkAgg(self.dataset.currentUSFigure(), self.root)
        self.canvas6.get_tk_widget().grid(column = 3, row = 2)
        '''

        ## show window again
        self.root.mainloop()





def main():

    interface = Interface()

if __name__ == '__main__': main()
