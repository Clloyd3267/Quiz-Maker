###################################################################################################
# Name        : Quiz-Maker-GUI.py
# Author(s)   : Andrew Southwick
# Description : The frontend of QuizMaker.py
###################################################################################################

import tkinter as tk
from tkinter import *
from tkinter import Frame, Tk, BOTH, Text, Menu, END, Label, Button, Entry, Radiobutton
from tkinter import filedialog


class MainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # Main Container that all "pages" will reside in
        container = tk.Frame(self)
        container.pack(fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Create a dictonary of all of the different frame "page" objects
        self.frames = {}
        for F in (StartPage, QuizPage, QuizPage2, ConfigFile):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the main page that is open when widow is produced
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        #label = tk.Label(self, text="This is the start page")
        #label.grid(row=0)

        Button(self, text = "Quiz Generating Page",
                    command = lambda: controller.show_frame("QuizPage")).grid()
        Button(self, text="Quiz Generating Page 2",
                            command = lambda: controller.show_frame("QuizPage2")).grid()
        Button(self, text="Configuration Page",
                            command = lambda: controller.show_frame("ConfigFile")).grid()



class ConfigFile(Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        #      SPECIALTIES = ["INT","MA" "Q",
        #                      "FTV", "CVR", "CR", "SIT"]
        #
        #    for specialties in SPECIALTIES:
        #         i=1
        #          i=i+1
        #           Label(text=specialties).grid(sticky='E', row=i)
        #

        Label(self, text='INT:').grid(sticky='E', row=1)
        Label(self, text='MA:').grid(sticky='E', row=2)
        Label(self, text='Q:').grid(sticky='E', row=3)
        Label(self, text='FTV:').grid(sticky='E', row=4)
        Label(self, text='CVR:').grid(sticky='E', row=5)
        Label(self, text='CR:').grid(sticky='E', row=6)
        Label(self, text='SIT:').grid(sticky='E', row=7)
        Label(self, text="Total:").grid(sticky='E', row=8)

        # The Min and Max Labels
        Label(self, text="Min").grid(sticky='N', row=0, column=1)
        Label(self, text="Max").grid(sticky='N', row=0, column=2)


        # Int Variables
        IntMin = IntVar(value=8)
        IntMax = IntVar(value=8)
        Entry(self, width=5, textvariable=IntMin).grid(sticky='N', row=1, column=1, padx=20, pady=5)
        Entry(self, width=5, textvariable=IntMax).grid(sticky='N', row=1, column=2, padx=20, pady=5)



        # CR Variables
        MaMin = IntVar(value=2)
        MaMax = IntVar(value=2)
        Entry(self, width=5, textvariable=MaMin).grid(sticky='N', row=2, column=1, padx=20, pady=5)
        Entry(self, width=5, textvariable=MaMax).grid(sticky='N', row=2, column=2, padx=20, pady=5)


        # CR Variables
        QMin = IntVar(value=2)
        QMax = IntVar(value=2)
        Entry(self, width=5, textvariable=QMin).grid(sticky='N', row=3, column=1, padx=20, pady=5)
        Entry(self, width=5, textvariable=QMax).grid(sticky='N', row=3, column=2, padx=20, pady=5)


        # FTV Variables
        FtvMin = IntVar(value=2)
        FtvMax = IntVar(value=2)
        Entry(self, width=5, textvariable=FtvMin).grid(sticky='N', row=4, column=1, padx=20, pady=5)
        Entry(self, width=5, textvariable=FtvMax).grid(sticky='N', row=4, column=2, padx=20, pady=5)


        # CVR Variables
        CvrMin = IntVar(value=2)
        CvrMax = IntVar(value=2)
        Entry(self, width=5, textvariable=CvrMin).grid(sticky='N', row=5, column=1, padx=20, pady=5)
        Entry(self, width=5, textvariable=CvrMax).grid(sticky='N', row=5, column=2, padx=20, pady=5)

        # CR Variables
        CrMin = IntVar(value=2)
        CrMax = IntVar(value=2)
        Entry(self, width=5,textvariable=CrMin).grid(sticky='N', row=6, column=1, padx=20, pady=5)
        Entry(self, width=5,textvariable=CrMax).grid(sticky='N', row=6, column=2, padx=20, pady=5)

        # SIT Variables
        SitMin = IntVar(value=2)
        SitMax = IntVar(value=2)
        Entry(self, width=5, state='normal',
                     textvariable=SitMin).grid(sticky='N', row=7, column=1, padx=20, pady=5)
        Entry(self, width=5, state='normal',
              textvariable=SitMax).grid(sticky='N', row=7, column=2, padx=20, pady=5)


        self.controller.bind("<Tab>", lambda e: self.OnTotal(IntMin, IntMax, MaMin, MaMax,
                                             QMin, QMax, FtvMin, FtvMax, CvrMin, CvrMax,
                                                CrMin, CrMax, SitMin, SitMax, self.AB, self.Check, self.Num2))

        self.controller.bind("<Return>", lambda e: self.OnTotal(IntMin, IntMax, MaMin, MaMax,
                                             QMin, QMax, FtvMin, FtvMax, CvrMin, CvrMax,
                                                CrMin, CrMax, SitMin, SitMax, self.AB, self.Check, self.Num2))

        #Label(text=var).grid(row=8, column=1)


        # Entry to grab # of questions wanted in quiz
        # NOTE: for variables to go through functions,
        # you must separate grid from main variable
        self.Num2 = IntVar(value=0)
        Num = Entry(self, width=5, state='disabled', textvariable=self.Num2)
        Num.grid(row=2, column=5, sticky=E)
        self.AB = IntVar(value=20)

        # adding a middle line to make it look nicer(?)
        for i in range(8):
            Label(self, text="|").grid(row=i, column=3, sticky="NESW", padx=20)

        # R-Buttons for how many questions they want in the quiz.
        Radiobutton(self, text="20 Question Quiz", variable=self.AB, value=20,
                    command=lambda: self.ABCheck(self.AB, Num,self.Num2)).grid(row=0, column=4, sticky=W)
        Radiobutton(self, text="15 Question Quiz", variable=self.AB, value=15,
                    command=lambda: self.ABCheck(self.AB, Num, self.Num2)).grid(row=1, column=4, sticky=W)
        Radiobutton(self, text="Define # Of Questions:", variable=self.AB, value=1,
                    command=lambda: self.ABCheck(self.AB, Num, self.Num2)).grid(row=2, column=4, sticky=W)

        # Checkbutton for whether ppl want A's and B's
        self.Check = IntVar(value=True)
        Checkbutton(self, text="Include A's and B's", variable=self.Check).grid(row=3, column=4, sticky=W, )


        Button(self, text="SAVE", command = lambda: controller.show_frame("StartPage")).grid(row=8, column=3, sticky=E)
        Button(self, text="Cancel", command = lambda: controller.show_frame("StartPage")).grid(row=8, column=4, sticky=W)

        self.OnTotal(IntMin, IntMax, MaMin, MaMax,
                 QMin, QMax, FtvMin, FtvMax, CvrMin, CvrMax,
                 CrMin, CrMax, SitMin, SitMax, self.AB, self.Check, self.Num2)


    def OnTotal(self, IntMin, IntMax, MaMin, MaMax, QMin, QMax, FtvMin, FtvMax,
            CvrMin, CvrMax, CrMin, CrMax, SitMin, SitMax, AB, Check, Num):
        Num = Num.get()
        AB = AB.get()
        Check = Check.get()
        if AB == 1:
            AB = Num
        Min = 0
        Max = 0
        Min = IntMin.get()+MaMin.get()+QMin.get()+FtvMin.get()+CvrMin.get()+CrMin.get()+SitMin.get()
        Max = IntMax.get()+MaMax.get()+QMax.get()+FtvMax.get()+CvrMax.get()+CrMax.get()+SitMax.get()
        MinLabel = Label(self, text=Min)
        MinLabel.grid(row=8, column=1, sticky=N)
        MaxLabel = Label(self, text=Max)
        MaxLabel.grid(row=8, column=2, sticky=N)
        if Min <= AB:
            MinLabel.config(fg='green')
        else:
            MinLabel.config(fg='red')



        if Check == 1:
            if Max >= AB+10:
                MaxLabel.config(fg='green')
            else:
                MaxLabel.config(fg='red')
        else:
            if Max >= AB:
                MaxLabel.config(fg='green')
            else:
                MaxLabel.config(fg='red')

    def OnClick(self, master):
        master.destroy()
        main(GridDemo)


    def CheckSit(self, SIT, SitMin, SitMax):
        if SIT.get() == 2:
            SitMin.configure(state='disabled')
            SitMax.configure(state='disabled')
        else:
            SitMin.configure(state='normal')
            SitMax.configure(state='normal')

    # check to see if we need to change the entry widget's state
    def ABCheck(self, AB, Num, Num2):
        if AB.get() == 1:
            Num.configure(state='normal')
        else:
            Num.configure(state='disabled')
            Num2 = 0
            return Num2





class QuizPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        Label(self, text = "Generating Quiz Page").grid()
        Button(self, text = "Start Page",
                           command = lambda: controller.show_frame("StartPage")).grid()

        column = 2
        OptionMenu(self, "hello", 1,2,3).grid(row=2, column=2)
        OptionMenu(self, "hello", 1,2,3).grid(row=2, column=3)
        OptionMenu(self, "hello", 1,2,3).grid(row=2, column=4)

        Button(self, text="Add Range", command = lambda: AddRange(column)).grid(row=2, column=1)

        def AddRange(column):
            column= column + 1
            OptionMenu(self, "hello", 1, 2, 3).grid(row=column, column=2)
            OptionMenu(self, "hello", 1, 2, 3).grid(row=column, column=3)
            OptionMenu(self, "hello", 1, 2, 3).grid(row=column, column=4)


class QuizPage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        Label(self, text = "Generating Quiz Page").grid()
        Button(self, text = "Start Page",
                           command = lambda: controller.show_frame("StartPage")).grid()

        column = 2
        Entry(self, width=5).grid(row=2, column=2, padx=2, pady=5)
        Label(self, text="Corinthians").grid(row=2, column=3)
        Entry(self, width=5).grid(row=2, column=4, padx=20, pady=5)
        Entry(self, width=5).grid(row=2, column=5, padx=20, pady=5)

        Button(self, text="Add Range", command = lambda: AddRange(column)).grid(row=2, column=1)

        def AddRange(column):
            column= column + 1
            Entry(self, width=5).grid(row=column, column=2, padx=2, pady=5)
            Label(self, text="Corinthians").grid(row=column, column=3)
            Entry(self, width=5).grid(row=column, column=4, padx=20, pady=5)
            Entry(self, width=5).grid(row=column, column=5, padx=20, pady=5)


if __name__ == "__main__":
    app = MainApp()
    app.minsize(600, 300)
    app.resizable(False, False)
    app.mainloop()
