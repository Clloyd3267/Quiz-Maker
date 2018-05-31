###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import xlsxwriter # Used to write quizzes to excel files
import re # Used for pattern matching
import time # Used to time exception speed
import random # Used for random numbers and random choice

# Project Imports
from QuestionList import *
from MaterialList import *
from UniqueList import *
from ConfigList import *

start_time = time.time() # Start a timer

class QuizMaker:
    """
    A class to perform the high level functions in quiz creation.

    Attributes:
        ql (QuestionList): Object of type QuestionList.
        ml (MaterialList): Object of type MaterialList.
        cl (ConfigList): Object of type ConfigList.
    """

    def __init__(self, questionFileName = "questions.xlsx", materialFileName = "material.xlsx", uniqueWordsFileName = "uniqueWords.xlsx"):
        """
        The constructor for class QuizMaker.
        """

        self.ql = QuestionList(questionFileName)  # Create an object of type QuestionList
        self.ml = MaterialList(materialFileName)  # Create an object of type MaterialList
        self.uL = UniqueList(uniqueWordsFileName) # Create an object of type UniqueList
        self.cl = ConfigList()    # Create an object of type ConfigList

        self.configDataName = None
        self.usedQuestions = None
        self.allValidQuestions = None
        self.questionTypesUsed = None
        self.allQuestionTypes = None
        self.questionNum = None

    def generateQuizzes(self, numQuizzes, arrayOfRanges, configDataName, outputFilename):
        """
        Function to generate quizzes.

        Parameters:
            numQuizzes (int): The number of quizzes wanted.
            arrayOfRanges (array of str): Ranges to use for quiz generation.
            configDataName (str): Name of config data file..
        """

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

        self.configDataName = configDataName

        quizzes = [] # Array to store quizzes

        # Dict to track the used questions
        self.usedQuestions = {"MA":[], "CR":[], "CVR":[], "Q":[], "FTV":[], "INT":[]}
        # Find all questions within the range and add them to allValidQuestions dict
        self.allValidQuestions = self.findValidQuestions(arrayOfRanges)

        quizNum = 0 # Iterator for number of quizzes
        while quizNum != numQuizzes:

            # Generate 50 quizzes
            quizSelection = []
            quizRatings = []
            i = 0
            while i != 25:
                quiz = self.generateQuiz()
                rating = self.rateQuiz(quiz)
                quizSelection.append(quiz)
                quizRatings.append(rating)
                i += 1

            minIndex = quizRatings.index(min(quizRatings))
            quiz = quizSelection[minIndex]

            quizzes.append(quiz) # Add the quiz to the list of quizzes
            quizNum += 1 # Increment quiz number

        self.debugQuizGen(quizzes, configDataName) # Function to debug quizzes
        self.exportQuizzes(quizzes, outputFilename) # Function to export quizzes to excel

    def exportQuizzes(self, quizzes, outputFilename):
        """
        Function to export quizzes to excel file.

        Parameters:
           quizzes (array of quiz objects): All of the quizzes to be outputted.
        """

        workbook = xlsxwriter.Workbook(outputFilename)
        worksheet = workbook.add_worksheet()
        allCellFormat = workbook.add_format({'font_size': 11, 'text_wrap': 1, 'valign': 'top', 'border': 1})
        bold = workbook.add_format({'bold': 1})

        # Size columns
        colLengthList = [5, 9, 38, 65, 12, 3, 3] # Lengths of columns in output file
        for i, width in enumerate(colLengthList):
            worksheet.set_column(i, i, width)

        i = 1
        j = 1
        for quiz in quizzes:
            i += 1
            worksheet.write("A" + str(i),"Quiz " + str(j))
            i += 1
            j += 1

            for question in quiz:
                worksheet.write("A" + str(i), question.questionNumber, allCellFormat)
                worksheet.write("B" + str(i), question.questionType, allCellFormat)
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
        rMatch = re.search(r'According\sto.*Chapter', myString, re.IGNORECASE)
        qMatch = re.search(r'Quote\sto.*Chapter', myString, re.IGNORECASE)
        if rMatch or qMatch:
            result.append(myString)
            return result
        for character in myString:
            if character.isalnum() or character in self.uL.partOfWord:
                word += character
            elif self.uL.isWordUnique(word):
                    result.append(boldFormat)
                    result.append(word)
                    result.append(character)
                    word = ""
            else:
                if word:
                    result.append(word)
                result.append(character)
                word = ""
        if word:
            if self.uL.isWordUnique(word):
                result.append(boldFormat)
                result.append(word)
            else:
                result.append(word)

        return result

    def debugQuizGen(self, quizzes, configDataName):
        """
        Function to debug quizzes.

        Parameters:
            quizzes (array of quiz): All of the quizzes to be debugged.
            configDataName (str): Name of config data file.
        """

        # Remove function later
        numNextToEachOther = {"MA":0, "CR":0, "CVR":0, "Q":0, "FTV":0, "INT":0}
        self.allQuestionTypes = ["MA", "CR", "CVR", "Q", "FTV", "INT"]
        if self.ql.isGospel:
            numNextToEachOther["SIT"] = 0
            self.allQuestionTypes.append("SIT")

        for quiz in quizzes:
            self.questionNum = 0
            while self.questionNum != int(self.cl.configList[self.configDataName].numberOfQuestions) - 1:
                for qType in self.allQuestionTypes:
                    if quiz[self.questionNum].questionType.find(qType) != -1 and quiz[self.questionNum + 1].questionType.find(qType) != -1:
                        numNextToEachOther[qType] += 1
                self.questionNum += 1
        total = 0
        for key in list(numNextToEachOther.keys()):
            if key != "INT":
                total += numNextToEachOther[key]
            print(key + ": " + str(numNextToEachOther[key]))
        print("Total:",total)

    def rateQuiz(self, quiz):
        score = 0
        previousType = ""

        for question in quiz:
            currentType = self.findMainType(question.questionType)
            if currentType == previousType:
                score += 1
            previousType = currentType
        return score

    def minMet(self, questionTypesUsed):
        """
        Function to check if min is met for all questions.

        Parameters:
            questionTypesUsed (dict): Number of times each type of question was used.

        Returns:
            True (bool): Min has been met.
            False (bool): Min has not been met.
        """

        for key in list(questionTypesUsed.keys()):
            if key == "INT":
                continue
            if int(questionTypesUsed[key]) != int(self.cl.configList[self.configDataName].typeMinMax[key][0]):
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

        validQuestions = {"INT":[], "CR":[], "CVR":[], "MA":[], "Q":[], "FTV":[]}

        if self.ql.isGospel:
            validQuestions["SIT"] = []

        for question in self.ql.questionDatabase:
            searchVerse = ",".join([question.questionBook, question.questionChapter, question.questionVerseStart])
            if not self.ml.isVerseInRange(searchVerse, arrayOfRanges):
                continue

            qMainType = self.findMainType(question.questionType)
            if qMainType == None:
                print(question.questionType)
            validQuestions[qMainType].append(question)

        for qType in validQuestions.keys():
            random.shuffle(validQuestions[qType])

        return validQuestions

    def findMainType(self, questionType):
        searchTypes = \
            {"INT":["INT", "INTF"],
             "CR":["CR", "CRMA"],
             "CVR":["CVR", "CVRMA"],
             "MA":["MA"],
             "Q":["Q", "Q2"],
             "FTV":["FTV", "FT2V", "F2V", "FT", "FTN"]}

        for qMainType in searchTypes.keys():
            for qType in searchTypes[qMainType]:
                if questionType.lower().find(qType.lower()) != -1:
                    return qMainType

    def fillMinimums(self, quiz):
        # func to fill the minimums of each type
        while self.questionNum != int(self.cl.configList[self.configDataName].numberOfQuestions):
            if self.minMet(self.questionTypesUsed):  # Check to see if all minimums have been filled
                break

            questionPicked = False  # Var to track if a question has been picked
            while not questionPicked:
                # Pick a random type of question
                randomQType = random.choice(list(self.allValidQuestions.keys()))

                # Check to see if question type is INT
                if randomQType == "INT":
                    continue
                # Check to see if question type has met it's minimum
                elif int(self.questionTypesUsed[randomQType]) == int(
                    self.cl.configList[self.configDataName].typeMinMax[randomQType][0]):
                    continue
                # Select a question from unused pile
                elif self.allValidQuestions[randomQType]:
                    selectedQuestion = random.choice(self.allValidQuestions[randomQType])
                    self.allValidQuestions[randomQType].remove(selectedQuestion)
                    self.usedQuestions[randomQType].append(selectedQuestion)
                # Select a question from used pile
                else:
                    selectedQuestion = random.choice(self.usedQuestions[randomQType])

                # Add question and iterate variables
                quiz.append(selectedQuestion)
                self.questionTypesUsed[randomQType] += 1
                questionPicked = True
                self.questionNum += 1

        self.questionTypesUsed["INT"] = 0  # Add INTs to dict for storing question type count
        numInts = 0  # Iterator for INT weight
        while numInts != int(self.cl.configList[self.configDataName].intWeight):
            self.allQuestionTypes.append("INT")
            numInts += 1

    def fillRemainingNumberedQuestions(self, quiz):
        # Loop for the rest of the numbered questions
        while self.questionNum != int(self.cl.configList[self.configDataName].numberOfQuestions):
            questionPicked = False  # Var to track if a question has been picked
            while not questionPicked:
                # Pick a random type of question
                randomQType = random.choice(self.allQuestionTypes)

                # Check to see if question type has met it's maximum
                if randomQType != "INT" and int(self.questionTypesUsed[randomQType]) == int(
                    self.cl.configList[self.configDataName].typeMinMax[randomQType][1]):
                    self.allQuestionTypes.remove(randomQType)
                    continue
                # Select a question from unused pile
                elif self.allValidQuestions[randomQType]:
                    selectedQuestion = random.choice(self.allValidQuestions[randomQType])
                    self.allValidQuestions[randomQType].remove(selectedQuestion)
                    self.usedQuestions[randomQType].append(selectedQuestion)
                # Select a question from used pile
                else:
                    selectedQuestion = random.choice(self.usedQuestions[randomQType])

                # Add question and iterate variables
                quiz.append(selectedQuestion)
                questionPicked = True
                self.questionTypesUsed[randomQType] += 1
                self.questionNum += 1

    def addQuestionNumbers(self, quiz):
        # Add question numbers to the non A and B questions
        self.questionNum = 1
        for question in quiz:
            question.questionNumber = str(self.questionNum)
            self.questionNum += 1

    def addAAndBQuestions(self, quiz):
        # Array to hold question types
        self.allQuestionTypes = ["MA", "CR", "CVR", "Q", "FTV", "INT"]
        # Check to see if year is a gospel
        if self.ql.isGospel:
            self.allQuestionTypes.append("SIT")

        self.questionNum = 1  # Iterator for question number
        questionIndex = 0  # Iterator for question index

        # Loop to fill A and B questions if any
        while self.questionNum != int(self.cl.configList[self.configDataName].numberOfQuestions) + 1:

            # If A and B questions are needed
            if self.questionNum >= 16 and self.cl.configList[self.configDataName].isAAndB:

                # If A and B questions should be filled using the same as the numbered question
                if self.cl.configList[self.configDataName].sameAB == "1":
                    qType = self.findMainType(quiz[questionIndex].questionType)
                    for subLetter in ["A", "B"]:
                        # Select a question from unused pile
                        if self.allValidQuestions[qType]:
                            selectedQuestion = random.choice(self.allValidQuestions[qType])
                            self.allValidQuestions[qType].remove(selectedQuestion)
                            self.usedQuestions[qType].append(selectedQuestion)
                        # Select a question from used pile
                        else:
                            selectedQuestion = random.choice(self.usedQuestions[qType])

                        selectedQuestion.questionNumber = str(self.questionNum) + subLetter
                        if subLetter == "A":
                            quiz.insert(questionIndex + 1, selectedQuestion)
                        elif subLetter == "B":
                            quiz.insert(questionIndex + 2, selectedQuestion)
                    questionIndex += 3  # Increment question index

                # If A and B questions should be filled using a random question type
                elif self.cl.configList[self.configDataName].randAB == "1":
                    for subLetter in ["A", "B"]:
                        questionPicked = False  # Var to track if a question has been picked
                        while not questionPicked:
                            # Pick a random type of question
                            randomQType = random.choice(self.allQuestionTypes)
                            # Check to see if question type has met it's maximum
                            if randomQType != "INT" and int(self.questionTypesUsed[randomQType]) == int(
                                self.cl.configList[self.configDataName].typeMinMax[randomQType][1]):
                                self.allQuestionTypes.remove(randomQType)
                                continue
                            # Select a question from unused pile
                            elif self.allValidQuestions[randomQType]:
                                selectedQuestion = random.choice(self.allValidQuestions[randomQType])
                                self.allValidQuestions[randomQType].remove(selectedQuestion)
                                self.usedQuestions[randomQType].append(selectedQuestion)
                            # Select a question from used pile
                            else:
                                selectedQuestion = random.choice(self.usedQuestions[randomQType])

                            selectedQuestion.questionNumber = str(self.questionNum) + subLetter
                            if subLetter == "A":
                                quiz.insert(questionIndex + 1, selectedQuestion)
                            elif subLetter == "B":
                                quiz.insert(questionIndex + 2, selectedQuestion)
                            questionPicked = True
                            self.questionTypesUsed[randomQType] += 1
                    questionIndex += 3  # Increment question index

            else:
                questionIndex += 1  # Increment question index

            self.questionNum += 1  # Increment question number

    def generateQuiz(self):
        quiz = []  # Create array to store a quiz
        # Dict to track the number of question types used
        self.questionTypesUsed = {"MA": 0, "CR": 0, "CVR": 0, "Q": 0, "FTV": 0}
        # Array to hold question types
        self.allQuestionTypes = ["MA", "CR", "CVR", "Q", "FTV"]
        # Check to see if year is a gospel
        if self.ql.isGospel:
            self.allQuestionTypes.append("SIT")
            self.questionTypesUsed["SIT"] = 0
        self.questionNum = 0  # Iterator for number of questions
        self.fillMinimums(quiz)
        self.fillRemainingNumberedQuestions(quiz)
        random.shuffle(quiz)  # Shuffle the numbered questions
        self.addQuestionNumbers(quiz)
        self.addAAndBQuestions(quiz)
        return quiz


if __name__ == "__main__":
    # CDL=> clean up main func
    qM = QuizMaker()                                                    # Create an object of type QuizMaker
    refRange = ["1 Corinthians,1,1-2 Corinthians,13,14"]                # Range used as an input
    qM.generateQuizzes(5, refRange, "default", 0)                     # Generate quizzes
    print("time elapsed: {:.2f}s".format(time.time() - start_time))     # Print program run time


    # Example help functions
    #help(Question)
    #help(Config)
    #help(QuestionList)
    #help(MaterialList)
    #help(ConfigList)
    #help(QuizMaker)