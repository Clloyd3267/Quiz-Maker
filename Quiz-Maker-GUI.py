###################################################################################################
# Name        : Quiz-Maker-GUI.py
# Author(s)   : Andrew Southwick
# Description : The frontend of QuizMaker.py
###################################################################################################




import tkinter as tk
from tkinter import *
from tkinter import Frame, Tk, BOTH, Text, Menu, END, Label, Button, Entry, Radiobutton
from tkinter import filedialog

class GridDemo(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Grid Demo")

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky='nwse')


        Button(self, text="Quiz-Maker Configuration",
                    command= ConfigFile).grid(row = 2, column = 1, columnspan = 2, sticky ='N',)


class ConfigFile(Frame):
    def __init__(self):
        tk.Frame.__init__(self)

  #      SPECIALTIES = ["INT","MA" "Q",
 #                      "FTV", "CVR", "CR", "SIT"]
#
    #    for specialties in SPECIALTIES:
   #         i=1
  #          i=i+1
 #           Label(text=specialties).grid(sticky='E', row=i)
#

        Label(text='INT:').grid(sticky='E', row=1)
        Label(text='MA:').grid(sticky='E', row=2)
        Label(text='Q:').grid(sticky='E', row=3)
        Label(text='FTV:').grid(sticky='E', row=4)
        Label(text='CVR:').grid(sticky='E', row=5)
        Label(text='CR:').grid(sticky='E', row=6)
        Label(text='SIT:').grid(sticky='E', row=7)

        # The Min and Max Labels
        Label(text="Min").grid(sticky='N', row=0, column=1)
        Label(text="Max").grid(sticky='N', row=0, column=2)


        # creating the entry boxes with a for loop
        for i in range(1,7):
            Entry(width=5,).grid(sticky='N', row=i, column=1, padx=20, pady=5)
            Entry(width=5).grid(sticky='N', row=i, column=2, padx=20, pady=5)

        SitMin = Entry(width=5, state='disabled')
        SitMin.grid(sticky='N', row=7, column=1, padx=20, pady=5)
        SitMax = Entry(width=5, state='disabled')
        SitMax.grid(sticky='N', row=7, column=2, padx=20, pady=5)


        # Entry to grab # of questions wanted in quiz
        # NOTE: for variables to go through functions,
        # you must separate grid from main variable
        Num = Entry(width=5, state='disabled',)
        Num.grid(row=2, column=5, sticky=E)
        self.AB = IntVar(value=20)

        # adding a middle line to make it look nicer(?)
        for i in range(8):
            Label(text="|").grid(row=i, column=3, sticky="NESW", padx=20)

        # R-Buttons for how many questions they want in the quiz.
        Radiobutton(text="20 Question Quiz", variable=self.AB, value=20,
                    command=lambda: self.ABCheck(self.AB, Num)).grid(row=0, column=4, sticky=W)
        Radiobutton(text="15 Question Quiz", variable=self.AB, value=15,
                    command=lambda: self.ABCheck(self.AB, Num)).grid(row=1, column=4, sticky=W)
        Radiobutton(text="Define # Of Questions:", variable=self.AB, value=1,
                    command=lambda: self.ABCheck(self.AB, Num)).grid(row=2, column=4, sticky=W)


        # Checkbutton for whether ppl want A's and B's
        self.Check = IntVar(value=True)
        Checkbutton(text="Include A's and B's", variable=self.Check).grid(row=3, column=4, sticky=W,)

        self.SITCheck = IntVar(value=2)

        Radiobutton(text="Narrative", variable=self.SITCheck, value=1,
                    command=lambda: self.CheckSit(self.SITCheck, SitMin, SitMax)).grid(row=8, column=1, sticky=W)
        Radiobutton(text="Epistle", variable=self.SITCheck, value=2,
                    command=lambda: self.CheckSit(self.SITCheck, SitMin, SitMax)).grid(row=8, column=2, sticky=W)

    def CheckSit(self, SIT, SitMin, SitMax):
        if SIT.get() == 2:
            SitMin.configure(state='disabled')
            SitMax.configure(state='disabled')
        else:
            SitMin.configure(state='normal')
            SitMax.configure(state='normal')

    # check to see if we need to change the entry widget's state
    def ABCheck(self, AB, Num):
        if AB.get() == 1:
            Num.configure(state='normal')
        else:
            Num.configure(state='disabled')


def main():
    ConfigFile().mainloop()


if __name__ == "__main__":
    app = Tk()
    app.minsize(600, 300)
    app.resizable(False, False)
    main()
