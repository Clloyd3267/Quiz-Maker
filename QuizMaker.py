###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################
import time
import random
from QuestionList import *
from MaterialList import *
from ConfigList import *
start_time = time.time()

class Quiz:
    def __init__(self):
        self.questions = []

    def printQuiz(self):
        for question in self.questions:
            question.printQuestion()

    def addQuestion(self, qQuestion):
        self.questions.append(qQuestion)


class QuizMaker:
    def __init__(self):
        self.ql = QuestionList()  # Create an object of type QuestionList
        self.ml = MaterialList()  # Create an object of type MaterialList
        self.cl = ConfigList()    # Create an object of type ConfigList

    def generateQuizzes(self, numQuizzes, arrayOfRanges, configDataName, isExtraQuestions):

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
        usedQuestions = {"MA":[], "CR":[], "CVR":[], "Q":[], "FTV":[], "INT":[]}
        # Find all questions within the range and add them to allValidQuestions dict
        allValidQuestions = self.findValidQuestions(arrayOfRanges)

        quizNum = 0 # Iterator for number of quizzes
        while quizNum != numQuizzes:
            quiz = Quiz() # Create a quiz object

            # Dict to track the number of question types used
            questionTypesUsed = {"MA": 0, "CR": 0, "CVR": 0, "Q": 0, "FTV": 0}
            # Array to hold question types
            allQuestionTypes = ["MA", "CR", "CVR", "Q", "FTV"]
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
                        questionIndex = allValidQuestions[randomQType].index(selectedQuestion)
                        selectedQuestion = allValidQuestions[randomQType][questionIndex]
                        allValidQuestions[randomQType].remove(selectedQuestion)
                        usedQuestions[randomQType].append(selectedQuestion)
                    # Select a question from used pile
                    else:
                        selectedQuestion = random.choice(usedQuestions[randomQType])

                    # Add question and iterate variables
                    quiz.addQuestion(selectedQuestion)
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
                        questionIndex = allValidQuestions[randomQType].index(selectedQuestion)
                        selectedQuestion = allValidQuestions[randomQType][questionIndex]
                        allValidQuestions[randomQType].remove(selectedQuestion)
                        usedQuestions[randomQType].append(selectedQuestion)
                    # Select a question from used pile
                    else:
                        selectedQuestion = random.choice(usedQuestions[randomQType])

                    # Add question and iterate variables
                    quiz.addQuestion(selectedQuestion)
                    questionPicked = True
                    questionTypesUsed[randomQType] += 1
                    questionNum += 1

            random.shuffle(quiz.questions) # Shuffle the numbered questions
            quizzes.append(quiz) # Add the quiz to the list of quizzes
            quizNum += 1 # Increment quiz number
        self.debugQuizGen(quizzes, configDataName)

        # Make an array of question numbers to loop through
        # for i in range(1, self.cl.configList[configDataName].numberOfQuestions + 1):
        #     if i >= 16 and self.cl.configList[configDataName].isAAndB:
        #         questionNums.append(str(i))
        #         questionNums.append(str(i) + "A")
        #         questionNums.append(str(i) + "B")
        #     else:
        #         questionNums.append(str(i))


    def debugQuizGen(self, quizzes, configDataName):
        numNextToEachOther = {"MA":0, "CR":0, "CVR":0, "Q":0, "FTV":0, "INT":0}
        allQuestionTypes = ["MA", "CR", "CVR", "Q", "FTV", "INT"]
        if self.ql.isGospel:
            numNextToEachOther["SIT"] = 0
            allQuestionTypes.append("SIT")

        for quiz in quizzes:
            # print(len(quiz.questions))
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
        for key in list(questionTypesUsed.keys()):
            if key == "INT":
                continue
            if int(questionTypesUsed[key]) != int(self.cl.configList[configDataName].typeMinMax[key][0]):
                return False
        return True

    def findValidQuestions(self, arrayOfRanges):
        validQuestions = {"INT":[],"MA":[], "CR":[], "CVR":[], "Q":[], "FTV":[]}
        types = ["INT", "MA", "CR", "CVR", "Q", "FTV"]
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

        return validQuestions

    def printQuestions(self, validQuestions):
        for qType in list(validQuestions.keys()):
            print(qType)
            for question in validQuestions[qType]:
                question.printQuestion()

if __name__ == "__main__":
    qM = QuizMaker()
    refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"]
    qM.generateQuizzes(1, refRange, "default", 0)
    print("time elapsed: {:.2f}s".format(time.time() - start_time))

    # CDL=> clean up main funcs

    # Example help functions
    #help(Question)
    #help(Config)
    #help(QuestionList)
    #help(MaterialList)
    #help(ConfigList)
    #help(QuizMaker)
