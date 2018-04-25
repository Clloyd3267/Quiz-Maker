###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

# External Imports
import xlsxwriter # Used to write quizzes to excel files
import time # Used to time exception speed
import random # Used for random numbers and random choice

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

    def printQuiz(self):
        """
        Function to print the quizzes.
        """

        for question in self.questions:
            question.printQuestion()


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
        self.ul = UniqueList()
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

        workbook = xlsxwriter.Workbook('Quizzes.xlsx')
        worksheet = workbook.add_worksheet()
        cell_format1 = workbook.add_format({'font_size': 10, 'text_wrap': 1, 'valign': 'top', 'border': 1})
        bold = workbook.add_format({'bold': 1})

        length_list = [3, 9, 38, 65, 12, 3, 3]
        for i, width in enumerate(length_list):
            worksheet.set_column(i, i, width)

        i = 1
        j = 1
        for quiz in quizzes:
            i += 1
            worksheet.write("A" + str(i),"Districts Practice " + str(j))
            i += 1
            j += 1

            for question in quiz.questions:
                worksheet.write("A" + str(i), question.questionNumber, cell_format1)
                if question.questionType == "MAN":
                    typeOfQuestion = "MA"
                else:
                    typeOfQuestion = question.questionType
                worksheet.write("B" + str(i), typeOfQuestion, cell_format1)
                if question.questionType == "MA" or question.questionType == "INT":
                    worksheet.write_rich_string("C" + str(i), *self.boldUniqueWords(question.questionQuestion, bold, cell_format1))
                else:
                    worksheet.write("C" + str(i), question.questionQuestion, cell_format1)
                worksheet.write_rich_string("D" + str(i), *self.boldUniqueWords(question.questionAnswer, bold, cell_format1))
                worksheet.write("E" + str(i), question.questionBook, cell_format1)
                worksheet.write("F" + str(i), question.questionChapter, cell_format1)
                worksheet.write("G" + str(i), question.questionVerseStart, cell_format1)
                i += 1


        workbook.close()

    def boldUniqueWords(self, myString, boldFormat, mainFormat):
        myString = ''.join([c for c in myString if c.isalnum() or c.isspace() or (c == "-") or c == "’"])
        result = []
        for word in myString.split():
            word += " "
            if self.ul.isWordUnique(word):
                result.append(boldFormat)
                result.append(word)
            else:
                result.append(word)
        result.append(mainFormat)
        return result

    def debugQuizGen(self, quizzes, configDataName):
        """
        Function to debug quizzes.

        Parameters:
            quizzes (array of quiz): All of the quizzes to be debugged.
            configDataName (str): Name of config data file.
        """

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
    # CDL=> clean up main funcs
    qM = QuizMaker()                                                    # Create an object of type QuizMaker
    refRange = ["1 Corinthians,1,1-2 Corinthians,13,14"]                # Range used as an input
    qM.generateQuizzes(10, refRange, "default", 0)                       # Generate quizzes
    print("time elapsed: {:.2f}s".format(time.time() - start_time))     # Print program run time


    # Example help functions
    #help(Question)
    #help(Config)
    #help(QuestionList)
    #help(MaterialList)
    #help(ConfigList)
    #help(QuizMaker)