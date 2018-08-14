###################################################################################################
# Name        : SimplifiedQuizMakerGui.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Gui to meet the needs of those less tech-savvy
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import time # Used to time exception speed
from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk

# Project Imports
from QuizMaker import *


class MainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        Label(self, text="# of Quizzes: ").grid(row=1, column=1)
        NumQuizzes = IntVar(value=1)
        Entry(self, width=3, textvariable=NumQuizzes).grid(sticky=W, row=1, column=2, padx=5, pady=5)

        Label(self, text="Range: ").grid(sticky=E, row=2, column=1)
        DefaultRange = StringVar(value="John,1,1-John,21,25")
        Entry(self, width=40, textvariable=DefaultRange).grid(row=2, column=2, padx=5, pady=5)

        Button(self, text="Create Quizzes",
               command=lambda: self.GenerateQuizzes(DefaultRange, NumQuizzes)).grid(
            sticky=W, row=4, column=1, padx=5, pady=5, columnspan=2)

    def Output(self):
        ftypes = [('Excel files', '*.xlsx')]
        date = time.strftime("%Y_%m_%d")
        fileName = Path(date + "_Quizzes.xlsx")
        dlg = filedialog.asksaveasfilename(filetypes = ftypes, initialdir = Path.home() / "Documents", initialfile = fileName)
        return dlg

    def GenerateQuizzes(self, MatRange, NumQuizzes):
        outputFilename = self.Output()
        if outputFilename == "":
            return

        NumQuizzes = NumQuizzes.get()
        qM = QuizMaker()  # Create an object of type QuizMaker
        MatRange = MatRange.get()
        refRange = [MatRange]  # Range used as an input
        qM.generateQuizzes(NumQuizzes, refRange, outputFilename)  # Generate quizzes
        messagebox.showinfo("Finished!", "Quizzes have been generated!")


if __name__ == "__main__":
    app = MainApp()
    app.minsize(300, 100)
    app.title("Quiz Maker - Bible Quizzing")
    app.wm_iconbitmap('../Data Files/myicon.ico')
    app.mainloop()