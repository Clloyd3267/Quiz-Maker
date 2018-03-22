###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

import random as random
from QuestionList import *
from MaterialList import *
from ConfigList import *


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

    def generateQuizzes(self, NumQuizzes, arrayOfRanges, configDataName, isExtraQuestions):

        usedQuestions = {"MA":[], "CR":[], "CVR":[], "Q":[], "FTV":[]}
        # quizzes = []
        # extraQuestions = []
        numIntsWanted = 5
        questionNums = []

        if NumQuizzes < 0:
            print("Error!!! Invalid Number of Quizzes")

        allValidQuestions = self.findValidQuestions(arrayOfRanges)
        validQuestions = dict(allValidQuestions)
        del validQuestions["INT"]

        allQuestionTypes = ["MA", "CR", "CVR", "Q", "FTV"]
        questionTypesUsed = {"MA":0, "CR":0, "CVR":0, "Q":0, "FTV":0, "INT":0}
        if self.ql.isGospel:
            questionTypesUsed["SIT"] = 0
            allQuestionTypes.append("SIT")

        quiz = Quiz()
        numInts = 0
        while numInts != numIntsWanted:
            allQuestionTypes.append("INT")
            numInts += 1


        i = 1
        while i != int(self.cl.configList[configDataName].numberOfQuestions):
            if self.minMet(configDataName, questionTypesUsed):
                break
            questionTypePicked = False

            while not questionTypePicked:
                randomQType = random.choice(list(validQuestions.keys()))
                if int(questionTypesUsed[randomQType]) == int(self.cl.configList[configDataName].typeMinMax[randomQType][0]):
                    continue
                else:
                    if validQuestions[randomQType]:
                        selectedQuestion = random.choice(validQuestions[randomQType])
                        questionIndex = validQuestions[randomQType].index(selectedQuestion)
                        selectedQuestion = validQuestions[randomQType][questionIndex]
                        validQuestions[randomQType].remove(selectedQuestion)
                        usedQuestions[randomQType].append(selectedQuestion)
                        questionTypesUsed[randomQType] += 1
                        questionTypePicked = True
                    else:
                        selectedQuestion = random.choice(usedQuestions[randomQType])
                        questionTypesUsed[randomQType] += 1
                        questionTypePicked = True
                    quiz.addQuestion(selectedQuestion)
            i += 1

        usedQuestions["INT"] = []

        while i != int(self.cl.configList[configDataName].numberOfQuestions):
            questionTypePicked = False

            while not questionTypePicked:
                randomQType = random.choice(allQuestionTypes)
                if randomQType != "INT" and int(questionTypesUsed[randomQType]) == int(
                    self.cl.configList[configDataName].typeMinMax[randomQType][1]):
                    allQuestionTypes.remove(randomQType)
                    continue
                else:
                    if allValidQuestions[randomQType]:
                        selectedQuestion = random.choice(allValidQuestions[randomQType])
                        questionIndex = allValidQuestions[randomQType].index(selectedQuestion)
                        selectedQuestion = allValidQuestions[randomQType][questionIndex]
                        allValidQuestions[randomQType].remove(selectedQuestion)
                        usedQuestions[randomQType].append(selectedQuestion)
                        questionTypesUsed[randomQType] += 1
                        questionTypePicked = True
                    else:
                        selectedQuestion = random.choice(usedQuestions[randomQType])
                        questionTypesUsed[randomQType] += 1
                        questionTypePicked = True
                    quiz.addQuestion(selectedQuestion)
                i += 1

        # for i in range(15, configDataName].numberOfQuestions):
        #
        #
        #
        #     if allValidQuestions[randomQType]:
        #         selectedQuestion = random.choice(allValidQuestions[randomQType])
        #         questionIndex = allValidQuestions[randomQType].index(selectedQuestion)
        #         selectedQuestion = allValidQuestions[randomQType][questionIndex]
        #         allValidQuestions[randomQType].remove(selectedQuestion)
        #         usedQuestions[randomQType].append(selectedQuestion)
        #         questionTypesUsed[randomQType] += 1
        #         questionTypePicked = True
        #     else:
        #         selectedQuestion = random.choice(usedQuestions[randomQType])
        #         questionTypesUsed[randomQType] += 1
        #         questionTypePicked = True
        #     quiz.addQuestion(selectedQuestion)

        print("I =",i)
        quiz.printQuiz()
        # quizzes.append(quiz)

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
            # print(searchVerse)
            if not self.ml.isVerseInRange(searchVerse, arrayOfRanges):
                continue

            for qType in types:
                if not question.questionType.find(qType):
                    # print(question.questionType, qType)
                    validQuestions[qType].append(question)

        return validQuestions

    def printQuestions(self, validQuestions):
        for qType in list(validQuestions.keys()):
            print(qType)
            for question in validQuestions[qType]:
                question.printQuestion()







qM = QuizMaker()
refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"] # Test range for checkRange func
qM.generateQuizzes(1, refRange, "default", 0)

# dict1 =  qM.findValidQuestions(refRange)
# qM.printQuestions(dict1)





        # Make an array of question numbers to loop through
        # for i in range(1, self.cl.configList[configDataName].numberOfQuestions + 1):
        #     if i >= 16 and self.cl.configList[configDataName].isAAndB:
        #         questionNums.append(str(i))
        #         questionNums.append(str(i) + "A")
        #         questionNums.append(str(i) + "B")
        #     else:
        #         questionNums.append(str(i))



        # shuffle(validQuestions)

        # for question in validQuestions:
        #     if question in usedQuestions:
        #         found = True
        # if not found:
        #










# if __name__ == "__main__":

    # Example help functions
    # help(Question)
    # help(Chapter)
    # help(QuestionList)
    # help(MaterialList)

    # ql1 = QuestionList() # Create an object of type QuestionList
    # ml1 = MaterialList() # Create an object of type MaterialList
    # cl1 = ConfigList()   # Create an object of type ConfigList

    # cl1.printConfigData() # Print all of the Configuration Data

    # refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"] # Test range for checkRange func
    # print("Range Valid: " + str(ml1.checkRange(refRange))) # Testing checkRange func
    # ml1.printMaterial()  # Print the Material list to ensure it is working