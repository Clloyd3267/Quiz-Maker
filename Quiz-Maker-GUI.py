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
               command=ConfigFile).grid(row=2, column=1, columnspan=2, sticky='N', )


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


        # Int Variables
        IntMin = IntVar(value=8)
        IntMax = IntVar(value=8)
        Entry(width=5, textvariable=IntMin).grid(sticky='N', row=1, column=1, padx=20, pady=5)
        Entry(width=5, textvariable=IntMax).grid(sticky='N', row=1, column=2, padx=20, pady=5)



        # CR Variables
        MaMin = IntVar(value=2)
        MaMax = IntVar(value=2)
        Entry(width=5, textvariable=MaMin).grid(sticky='N', row=2, column=1, padx=20, pady=5)
        Entry(width=5, textvariable=MaMax).grid(sticky='N', row=2, column=2, padx=20, pady=5)


        # CR Variables
        QMin = IntVar(value=2)
        QMax = IntVar(value=2)
        Entry(width=5, textvariable=QMin).grid(sticky='N', row=3, column=1, padx=20, pady=5)
        Entry(width=5, textvariable=QMax).grid(sticky='N', row=3, column=2, padx=20, pady=5)


        # FTV Variables
        FtvMin = IntVar(value=2)
        FtvMax = IntVar(value=2)
        Entry(width=5, textvariable=FtvMin).grid(sticky='N', row=4, column=1, padx=20, pady=5)
        Entry(width=5, textvariable=FtvMax).grid(sticky='N', row=4, column=2, padx=20, pady=5)


        # CVR Variables
        CvrMin = IntVar(value=2)
        CvrMax = IntVar(value=2)
        Entry(width=5, textvariable=CvrMin).grid(sticky='N', row=5, column=1, padx=20, pady=5)
        Entry(width=5, textvariable=CvrMax).grid(sticky='N', row=5, column=2, padx=20, pady=5)

        # CR Variables
        CrMin = IntVar(value=2)
        CrMax = IntVar(value=2)
        Entry(width=5,textvariable=CrMin).grid(sticky='N', row=6, column=1, padx=20, pady=5)
        Entry(width=5,textvariable=CrMax).grid(sticky='N', row=6, column=2, padx=20, pady=5)

        # SIT Variables
        SitMin = IntVar(value=2)
        SitMax = IntVar(value=2)
        Entry(width=5, state='normal',
                     textvariable=SitMin).grid(sticky='N', row=7, column=1, padx=20, pady=5)
        Entry(width=5, state='normal',
              textvariable=SitMax).grid(sticky='N', row=7, column=2, padx=20, pady=5)


        Button(text="Total", command=lambda: self.OnTotal(
            IntMin, IntMax, MaMin, MaMax, QMin, QMax, FtvMin, FtvMax,
            CvrMin, CvrMax, CrMin, CrMax, SitMin, SitMax,)).grid(row=8, column=0,)

        #Label(text=var).grid(row=8, column=1)


        # Entry to grab # of questions wanted in quiz
        # NOTE: for variables to go through functions,
        # you must separate grid from main variable
        Num = Entry(width=5, state='disabled', )
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
        Checkbutton(text="Include A's and B's", variable=self.Check).grid(row=3, column=4, sticky=W, )


        Button(text="SAVE", command=lambda: self.OnClick()).grid(row=8, column=3, sticky=E)
        Button(text="Cancel", command=lambda: self.OnClick()).grid(row=8, column=4, sticky=W)

    def OnTotal(self, IntMin, IntMax, MaMin, MaMax, QMin, QMax, FtvMin, FtvMax,
            CvrMin, CvrMax, CrMin, CrMax, SitMin, SitMax,):
        Min = 0
        Max = 0
        Min = IntMin.get()+MaMin.get()+QMin.get()+FtvMin.get()+CvrMin.get()+CrMin.get()+SitMin.get()
        Max = IntMax.get()+MaMax.get()+QMax.get()+FtvMax.get()+CvrMax.get()+CrMax.get()+SitMax.get()
        Label(text=Min).grid(row=8, column=1, sticky=N)
        Label(text=Max).grid(row=8, column=2, sticky=N, padx=20)


    def OnClick(self):
        main(GridDemo())

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


def main(Name):
    Name.mainloop()


if __name__ == "__main__":
    app = Tk()
    app.minsize(600, 300)
    app.resizable(False, False)
    main(ConfigFile())
