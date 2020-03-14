import tkinter as tk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from dataset import CovidDataset

class Interface:

    def __init__(self):
        
        root = tk.Tk()
        #root.configure(background = "grey17")
        root.title("2019 nCov Tracker")
        root.geometry("600x400")
        #basic setup

        dataset = CovidDataset()

        
        canvas = FigureCanvasTkAgg(dataset.figure(), root)
        canvas.draw()

        canvas.get_tk_widget().pack()
        canvas._tkcanvas.pack()




        root.mainloop()

def main():
    interface = Interface()


if __name__ == '__main__':main()      