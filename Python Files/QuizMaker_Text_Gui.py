import time

# Project Imports
from QuizMaker import *


if __name__ == "__main__":
    global start_time
    start_time = time.time()
    qM = QuizMaker()

    print("{:.2f}s".format(time.time() - start_time), "- Init")

    qM.numQuestions = int(input("How many questions do you want - 30 or 20? "))
    #refRange = ["John,1,1-John,21,25"]
    #refRange = input("What is the range of material? "
                     #"(Press enter for all the material) ")
    mir = True
    refRange = []
    while mir == True:
        refRange = input("What is the range of material? "
                     "(Press Enter for all the material or 'h' for help on setting the material range) ")
        if refRange == "":
            refRange = ["John,1,1-John,21,25"]
            mir = False
        elif refRange == "h":
            print("\nEnter the material ranges in the format: 'BOOK,CHAPTER,VERSE-BOOK,CHAPTER,VERSE' "
                  "Enter as many of these ranges separated by a comma. \n"
                  "Example: 'John,1,1-John,21,25' \n\n")
        else:
            refRange = refRange.split()
            mir = False


    numQuizzes = int(input("How many quizzes do you want to generate? "))
    qM.generateQuizzes(numQuizzes, refRange)
    print("{:.2f}s".format(time.time() - start_time), "- Done")