###################################################################################################
# Name        : SimplifiedQuizMakerGui.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Gui to meet the needs of those less tech-savvy
###################################################################################################

from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox

from QuizMaker import *


class MainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        #container = tk.Frame(self)
        #container.master.rowconfigure(0, weight=1)
        #container.master.columnconfigure(0, weight=1)
        #container.grid(sticky=W + E + N + S)

        #root = Tk()
        menubar = Menu(self)
        self.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Select Question File", command=self.Question)
        filemenu.add_command(label = "Select Unique Words File", command = self.Question)
        filemenu.add_command(label = "Select Material File", command = self.Question)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)

        Label(self, text="# of Quizzes: ").grid(row=1, column=1)
        NumQuizzes = IntVar(value=1)
        Entry(self, width=3, textvariable=NumQuizzes).grid(sticky=W, row=1, column=2, padx=5, pady=5)

        Label(self, text="Range: ").grid(sticky=E, row=2, column=1)
        DefaultRange = StringVar(value="1 Corinthians,1,1-2 Corinthians,13,14")
        Entry(self, width=40, textvariable=DefaultRange).grid(row=2, column=2, padx=5, pady=5)

        Button(self, text="Create Quizzes",
               command=lambda: self.GenerateQuizzes(DefaultRange, NumQuizzes)).grid(
            sticky=W, row=4, column=1, padx=5, pady=5, columnspan=2)


    def Question(self):
        ftypes = [('Excel files', '*.xlsx'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        global QuestionFile
        QuestionFile = dlg.show()

    def Unique(self):
        ftypes = [('Excel files', '*.xlsx'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        global UniqueFile
        UniqueFile = dlg.show()

    def Material(self):
        ftypes = [('Excel files', '*.xlsx'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        global MaterialFile
        MaterialFile = dlg.show()

    def Output(self):
        ftypes = [('Excel files', '*.xlsx'), ('All files', '*')]
        dlg = filedialog.asksaveasfilename(filetypes = ftypes, initialfile = "Quizzes.xlsx")
        return dlg

    def GenerateQuizzes(self, MatRange, NumQuizzes):
        outputFilename = self.Output()
        if outputFilename == "":
            return

        global QuestionFile
        if QuestionFile == "":
            QuestionFile = "questions.xlsx"
        global UniqueFile
        if UniqueFile == "":
            UniqueFile = "uniqueWords.xlsx"
        global MaterialFile
        if MaterialFile == "":
            MaterialFile = "material.xlsx"

        NumQuizzes = NumQuizzes.get()
        qM = QuizMaker(QuestionFile, MaterialFile, UniqueFile)  # Create an object of type QuizMaker
        MatRange = MatRange.get()
        refRange = [MatRange]  # Range used as an input
        qM.generateQuizzes(NumQuizzes, refRange, "default", outputFilename)  # Generate quizzes
        messagebox.showinfo("Finished!", "Quizzes have been generated!")


def main():
    global QuestionFile
    global UniqueFile
    global MaterialFile
    global OutputFile
    QuestionFile = ""
    UniqueFile = ""
    MaterialFile = ""
    app = MainApp()
    app.minsize(300, 100)
    app.title("Quiz Maker - Bible Quizzing")
    app.wm_iconbitmap('../Data Files/myicon.ico')
    app.mainloop()


if __name__ == "__main__":
    main()