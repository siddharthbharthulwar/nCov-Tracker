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

        root.mainloop()


def main():

    interface = Interface()

if __name__ == '__main__':

    main()
