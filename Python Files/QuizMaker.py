###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

# External Imports
import xlsxwriter # Used to write quizzes to excel files
import re # Used for pattern matching
import time # Used to time exception speed
import random # Used for random numbers and random choice
from pathlib import Path # Used for file manipulation

# Project Imports
from QuestionList import *
from MaterialList import *
from UniqueList import *
from ConfigList import *

start_time = time.time() # Start a timer

class Quiz:
    """
    A class to store the attributes of a quiz.

    Attributes:
        questions (array of question obj): An array to store the questions.
    """

    def __init__(self):
        """
        The constructor for class Quiz.
        """
        self.questions = [] # An array to store the questions


class QuizMaker:
    """
    A class to perform the high level functions in quiz creation.

    Attributes:
        ql (QuestionList): Object of type QuestionList.
        ml (MaterialList): Object of type MaterialList.
        cl (ConfigList): Object of type ConfigList.
    """

    def __init__(self):
        """
        The constructor for class QuizMaker.
        """

        self.ql = QuestionList()  # Create an object of type QuestionList
        self.ml = MaterialList()  # Create an object of type MaterialList
        self.uL = UniqueList()
        self.cl = ConfigList()    # Create an object of type ConfigList

    def generateQuizzes(self, numQuizzes, arrayOfRanges, configDataName, isExtraQuestions):
        """
        Function to generate quizzes.

        Parameters:
            numQuizzes (int): The number of quizzes wanted.
            arrayOfRanges (array of str): Ranges to use for quiz generation.
            configDataName (str): Name of config data file.
            isExtraQuestions (bool): Whether extra questions are wanted.
        """
        # CDL=> Fix error with MA vs CRMA???

        # Error Checking
        if numQuizzes <= 0:
            print("Error!!! Invalid Number of Quizzes.")
            return
        elif not configDataName in list(self.cl.configList.keys()):
            print("Error!!! Config Data does not exist.")
            return
        elif not self.ml.checkRange(arrayOfRanges):
            print("Error!!! Ranges are invalid.")
            return
        elif not int(isExtraQuestions) in [0, 1]:
            print("Error!!! isExtraQuestions must be a bool value.")
            return

        quizzes = [] # Array to store quizzes

        # Dict to track the used questions
        usedQuestions = {"MAN":[], "CR":[], "CVR":[], "Q":[], "FTV":[], "INT":[]}
        # Find all questions within the range and add them to allValidQuestions dict
        allValidQuestions = self.findValidQuestions(arrayOfRanges)

        quizNum = 0 # Iterator for number of quizzes
        while quizNum != numQuizzes:
            quiz = Quiz() # Create a quiz object

            # Dict to track the number of question types used
            questionTypesUsed = {"MAN": 0, "CR": 0, "CVR": 0, "Q": 0, "FTV": 0}
            # Array to hold question types
            allQuestionTypes = ["MAN", "CR", "CVR", "Q", "FTV"]
            # Check to see if year is a gospel
            if self.ql.isGospel:
                allQuestionTypes.append("SIT")
                questionTypesUsed["SIT"] = 0

            numInts = 0 # Iterator for INT weight
            while numInts != int(self.cl.configList[configDataName].intWeight):
                allQuestionTypes.append("INT")
                numInts += 1

            questionNum = 0 # Iterator for number of questions
            # Loop to fill the minimums of each type
            while questionNum != int(self.cl.configList[configDataName].numberOfQuestions):
                if self.minMet(configDataName, questionTypesUsed): # Check to see if all minimums have been filled
                    break

                questionPicked = False # Var to track if a question has been picked
                while not questionPicked:
                    # Pick a random type of question
                    randomQType = random.choice(list(allValidQuestions.keys()))

                    # Check to see if question type is INT
                    if randomQType == "INT":
                        continue
                    # Check to see if question type has met it's minimum
                    elif int(questionTypesUsed[randomQType]) == int(self.cl.configList[configDataName].typeMinMax[randomQType][0]):
                        continue
                    # Select a question from unused pile
                    elif allValidQuestions[randomQType]:
                        selectedQuestion = random.choice(allValidQuestions[randomQType])
                        allValidQuestions[randomQType].remove(selectedQuestion)
                        usedQuestions[randomQType].append(selectedQuestion)
                    # Select a question from used pile
                    else:
                        selectedQuestion = random.choice(usedQuestions[randomQType])

                    # Add question and iterate variables
                    quiz.questions.append(selectedQuestion)
                    questionTypesUsed[randomQType] += 1
                    questionPicked = True
                    questionNum += 1

            questionTypesUsed["INT"] = 0 # Add INTs to dict for storing question type count

            # Loop for the rest of the numbered questions
            while questionNum != int(self.cl.configList[configDataName].numberOfQuestions):
                questionPicked = False # Var to track if a question has been picked
                while not questionPicked:
                    # Pick a random type of question
                    randomQType = random.choice(allQuestionTypes)

                    # Check to see if question type has met it's maximum
                    if randomQType != "INT" and int(questionTypesUsed[randomQType]) == int(
                        self.cl.configList[configDataName].typeMinMax[randomQType][1]):
                        allQuestionTypes.remove(randomQType)
                        continue
                    # Select a question from unused pile
                    elif allValidQuestions[randomQType]:
                        selectedQuestion = random.choice(allValidQuestions[randomQType])
                        allValidQuestions[randomQType].remove(selectedQuestion)
                        usedQuestions[randomQType].append(selectedQuestion)
                    # Select a question from used pile
                    else:
                        selectedQuestion = random.choice(usedQuestions[randomQType])

                    # Add question and iterate variables
                    quiz.questions.append(selectedQuestion)
                    questionPicked = True
                    questionTypesUsed[randomQType] += 1
                    questionNum += 1

            random.shuffle(quiz.questions)  # Shuffle the numbered questions
            random.shuffle(quiz.questions)  # Shuffle the numbered questions
            random.shuffle(quiz.questions)  # Shuffle the numbered questions
            random.shuffle(quiz.questions)  # Shuffle the numbered questions
            random.shuffle(quiz.questions)  # Shuffle the numbered questions

            # Add question numbers to the non A and B questions
            questionNum = 1
            for question in quiz.questions:
                question.questionNumber = str(questionNum)
                questionNum += 1
            # Array to hold question types
            allQuestionTypes = ["MAN", "CR", "CVR", "Q", "FTV", "INT"]
            # Check to see if year is a gospel
            if self.ql.isGospel:
                allQuestionTypes.append("SIT")

            questionNum = 1 # Iterator for question number
            questionIndex = 0 # Iterator for question index
            # Loop to fill A and B questions if any
            while questionNum != int(self.cl.configList[configDataName].numberOfQuestions) + 1:
                # If an A and B questions are needed
                if questionNum >= 16  and self.cl.configList[configDataName].isAAndB:

                    # If A and B questions should be filled using the same as the numbered question
                    if self.cl.configList[configDataName].sameAB == "1":
                        for qType in allQuestionTypes:
                            if quiz.questions[questionIndex].questionType.find(qType) != -1:
                                for subLetter in ["A", "B"]:
                                    # Select a question from unused pile
                                    if allValidQuestions[qType]:
                                        selectedQuestion = random.choice(allValidQuestions[qType])
                                        allValidQuestions[qType].remove(selectedQuestion)
                                        usedQuestions[qType].append(selectedQuestion)
                                    # Select a question from used pile
                                    else:
                                        selectedQuestion = random.choice(usedQuestions[qType])

                                    selectedQuestion.questionNumber = str(questionNum) + subLetter
                                    if subLetter == "A":
                                        quiz.questions.insert(questionIndex + 1, selectedQuestion)
                                    elif subLetter == "B":
                                        quiz.questions.insert(questionIndex + 2, selectedQuestion)

                    # If A and B questions should be filled using a random question type
                    if self.cl.configList[configDataName].randAB == "1":
                        for subLetter in ["A", "B"]:
                            questionPicked = False  # Var to track if a question has been picked
                            while not questionPicked:
                                # Pick a random type of question
                                randomQType = random.choice(allQuestionTypes)
                                # Check to see if question type has met it's maximum
                                if randomQType != "INT" and int(questionTypesUsed[randomQType]) == int(
                                    self.cl.configList[configDataName].typeMinMax[randomQType][1]):
                                    allQuestionTypes.remove(randomQType)
                                    continue
                                # Select a question from unused pile
                                elif allValidQuestions[randomQType]:
                                    selectedQuestion = random.choice(allValidQuestions[randomQType])
                                    allValidQuestions[randomQType].remove(selectedQuestion)
                                    usedQuestions[randomQType].append(selectedQuestion)
                                # Select a question from used pile
                                else:
                                    selectedQuestion = random.choice(usedQuestions[randomQType])

                                selectedQuestion.questionNumber = str(questionNum) + subLetter
                                if subLetter == "A":
                                    quiz.questions.insert(questionIndex + 1, selectedQuestion)
                                elif subLetter == "B":
                                    quiz.questions.insert(questionIndex + 2, selectedQuestion)
                                questionPicked = True
                                questionTypesUsed[randomQType] += 1
                    questionIndex += 3 # Increment question index
                else:
                    questionIndex += 1 # Increment question index
                questionNum += 1 # Increment question number
            quizzes.append(quiz) # Add the quiz to the list of quizzes
            quizNum += 1 # Increment quiz number

        self.debugQuizGen(quizzes, configDataName) # Function to debug quizzes
        self.exportQuizzes(quizzes) # Function to export quizzes to excel

    def exportQuizzes(self, quizzes):
        """
        Function to export quizzes to excel file.

        Parameters:
           quizzes (array of quiz objects): All of the quizzes to be outputted.
        """

        fileName = Path("../Quizzes.xlsx")
        workbook = xlsxwriter.Workbook(fileName)
        worksheet = workbook.add_worksheet()
        allCellFormat = workbook.add_format({'font_size': 10, 'text_wrap': 1, 'valign': 'top', 'border': 1})
        bold = workbook.add_format({'bold': 1})

        # Size columns
        colLengthList = [3, 9, 38, 65, 12, 3, 3] # Lengths of columns in output file
        for i, width in enumerate(colLengthList):
            worksheet.set_column(i, i, width)

        i = 1
        j = 1
        for quiz in quizzes:
            print("Debug")
            i += 1
            worksheet.write("A" + str(i),"Districts Practice " + str(j))
            i += 1
            j += 1

            for question in quiz.questions:
                worksheet.write("A" + str(i), question.questionNumber, allCellFormat)
                # CDL=> Remove fix later
                if question.questionType == "MAN":
                    typeOfQuestion = "MA"
                else:
                    typeOfQuestion = question.questionType
                worksheet.write("B" + str(i), typeOfQuestion, allCellFormat)
                worksheet.write_rich_string("C" + str(i), *self.boldUniqueWords(question.questionQuestion, bold), allCellFormat)
                worksheet.write_rich_string("D" + str(i), *self.boldUniqueWords(question.questionAnswer, bold), allCellFormat)
                worksheet.write("E" + str(i), question.questionBook, allCellFormat)
                worksheet.write("F" + str(i), question.questionChapter, allCellFormat)
                worksheet.write("G" + str(i), question.questionVerseStart, allCellFormat)
                i += 1

        workbook.close()

    def boldUniqueWords(self, myString, boldFormat):
        """
        Function to bold unique words in a particular string.

        Parameters:
            myString (str): The input string to be bolded.
            boldFormat (xlsxwriter format object): The format to be applied to unique words.
        """

        if myString == "":
            print(myString)
        result = []
        word = ""
        match = re.search(r'According\sto.*Chapter', myString, re.IGNORECASE)
        if match:
            result.append(myString)
            return result
        for character in myString:
            if character.isalnum() or character in self.uL.partOfWord:
                word += character
            elif word and self.uL.isWordUnique(word):
                    result.append(boldFormat)
                    result.append(word)
                    result.append(character)
                    word = ""
            else:
                if word:
                    result.append(word)
                result.append(character)
                word = ""
        return result

    def debugQuizGen(self, quizzes, configDataName):
        """
        Function to debug quizzes.

        Parameters:
            quizzes (array of quiz): All of the quizzes to be debugged.
            configDataName (str): Name of config data file.
        """

        # Remove function later
        numNextToEachOther = {"MAN":0, "CR":0, "CVR":0, "Q":0, "FTV":0, "INT":0}
        allQuestionTypes = ["MAN", "CR", "CVR", "Q", "FTV", "INT"]
        if self.ql.isGospel:
            numNextToEachOther["SIT"] = 0
            allQuestionTypes.append("SIT")

        for quiz in quizzes:
            questionNum = 0
            while questionNum != int(self.cl.configList[configDataName].numberOfQuestions) - 1:
                for qType in allQuestionTypes:
                    if quiz.questions[questionNum].questionType.find(qType) != -1 and quiz.questions[questionNum + 1].questionType.find(qType) != -1:
                        numNextToEachOther[qType] += 1
                questionNum += 1
        total = 0
        for key in list(numNextToEachOther.keys()):
            if key != "INT":
                total += numNextToEachOther[key]
            print(key + ": " + str(numNextToEachOther[key]))
        print("Total:",total)

    def minMet(self, configDataName, questionTypesUsed):
        """
        Function to check if min is met for all questions.

        Parameters:
            configDataName (str): Name of config data file.
            questionTypesUsed (dict): Number of times each type of question was used.

        Returns:
            True (bool): Min has been met.
            False (bool): Min has not been met.
        """

        for key in list(questionTypesUsed.keys()):
            if key == "INT":
                continue
            if int(questionTypesUsed[key]) != int(self.cl.configList[configDataName].typeMinMax[key][0]):
                return False
        return True

    def findValidQuestions(self, arrayOfRanges):
        """
        Function to find all valid questions in range.

        Parameters:
            arrayOfRanges (array of str): Ranges to search for questions in.

        Returns:
            validQuestions (dict): All valid questions within the range.
        """

        validQuestions = {"INT":[],"MAN":[], "CR":[], "CVR":[], "Q":[], "FTV":[]}
        types = ["INT", "MAN", "CR", "CVR", "Q", "FTV"]
        if self.ql.isGospel:
            types.append("SIT")
            validQuestions["SIT"] = []

        for question in self.ql.questionDatabase:
            searchVerse = ",".join([question.questionBook, question.questionChapter, question.questionVerseStart])
            if not self.ml.isVerseInRange(searchVerse, arrayOfRanges):
                continue

            for qType in types:
                if question.questionType.find(qType) != -1:
                    validQuestions[qType].append(question)

        for qType in types:
            random.shuffle(validQuestions[qType])
            random.shuffle(validQuestions[qType])

        return validQuestions


if __name__ == "__main__":
    # CDL=> clean up main func
    qM = QuizMaker()                                                    # Create an object of type QuizMaker
    refRange = ["1 Corinthians,1,1-2 Corinthians,13,14"]                # Range used as an input
    qM.generateQuizzes(50, refRange, "default", 0)                       # Generate quizzes
    print("time elapsed: {:.2f}s".format(time.time() - start_time))     # Print program run time


    # Example help functions
    #help(Question)
    #help(Config)
    #help(QuestionList)
    #help(MaterialList)
    #help(ConfigList)
    #help(QuizMaker)