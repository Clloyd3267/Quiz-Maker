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
        menubar.add_cascade(label="Upload", menu=filemenu)
        filemenu.add_command(label="Upload File", command=self.Question)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)

        Label(self, text="# of Quizzes: ").grid(row=1, column=1)
        NumQuizzes = IntVar(value=1)
        Entry(self, width=3, textvariable=NumQuizzes).grid(sticky=W, row=1, column=2, padx=5, pady=5)

        Label(self, text="Range: ").grid(sticky=E, row=2, column=1)
        DefaultRange = StringVar(value="1 Corinthians,1,1-2 Corinthians,13,14")
        Entry(self, width=40, textvariable=DefaultRange).grid(row=2, column=2, padx=5, pady=5)

        ABCheck = IntVar(value=1)
        Checkbutton(self, text="Include A's and B's", variable=ABCheck).grid(row=3, column=2, sticky=W, )

        Button(self, text="Create Quizzes",
               command=lambda: self.GenerateQuizzes(DefaultRange, ABCheck, NumQuizzes)).grid(
            sticky=W, row=4, column=1, padx=5, pady=5, columnspan=2)


    def Question(self):
        ftypes = [('Excel files', '*.xlsx'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        global ABCQuestionFile
        ABCQuestionFile = dlg.show()



    def GenerateQuizzes(self, MatRange, ABCheck, NumQuizzes):
        global ABCQuestionFile
        if ABCQuestionFile == '':
            messagebox.showerror("Error!", "Please Upload Question File!")
            return

        ABCheck = ABCheck.get()
        NumQuizzes = NumQuizzes.get()
        qM = QuizMaker()  # Create an object of type QuizMaker
        MatRange = MatRange.get()
        print(ABCheck)
        refRange = [MatRange]  # Range used as an input
        qM.generateQuizzes(NumQuizzes, refRange, "default", ABCheck)  # Generate quizzes
        print("time elapsed: {:.2f}s".format(time.time() - start_time))



def main():
    global ABCQuestionFile
    ABCQuestionFile = ''
    app = MainApp()
    app.minsize(300, 200)
    app.mainloop()


if __name__ == "__main__":
    main()