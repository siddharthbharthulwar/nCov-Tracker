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
        root.title("2019 nCov Statistical Toolkit")
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.state("zoomed")
        root.configure(bg = "white")

        dataset = CovidDataset()

        canvas = FigureCanvasTkAgg(dataset.currentWorldFigure(), root)
        canvas.get_tk_widget().grid(column = 1, row = 1)
        
        
        canvas2 = FigureCanvasTkAgg(dataset.worldPrediction(4), root)
        canvas2.get_tk_widget().grid(column = 1, row = 2)

        canvas3 = FigureCanvasTkAgg(dataset.worldDifferential(), root)
        canvas3.get_tk_widget().grid(column = 2, row = 1)
        

        root.mainloop()


def main():

    interface = Interface()

if __name__ == '__main__':

    main()
