###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

from QuestionList import *
from MaterialList import *
from ConfigList import *

if __name__ == "__main__":

    # Example help functions
    # help(Question)
    # help(Chapter)
    # help(QuestionList)
    # help(MaterialList)

    ql1 = QuestionList() # Create an object of type QuestionList
    ml1 = MaterialList() # Create an object of type QuestionList
    cl1 = ConfigList()   # Create an object of type QuestionList

    # cl1.printConfigData() # Print all of the Configuration Data

    # refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"] # Test range for checkRange func
    # print("Range Valid: " + str(ml1.checkRange(refRange))) # Testing checkRange func
    # ml1.printMaterial()  # Print the Material list to ensure it is working