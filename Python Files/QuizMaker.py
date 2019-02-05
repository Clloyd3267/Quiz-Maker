###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import xlsxwriter # Used to write quizzes to excel files
import re # Used for pattern matching
import datetime # Used to time exception speed
import time
import random # Used for random numbers and random choice

# Project Imports
from QuestionList import *
from MaterialList import *

class QuizMaker:
    """
    A class to perform the high level functions in quiz creation.

    Attributes:
        qL (QuestionList): Object of type QuestionList.
    """

    def __init__(self, questionFileName = "Questions.xlsx"):
        """
        The constructor for class QuizMaker.

        Parameters:
            questionFileName (str): The name of the Question File (Defaults to "Questions.xlsx").
        """

        self.qL = QuestionList(questionFileName)  # Create an object of type QuestionList
        self.numQuestions = 20

    ####################################################################################################################
    # Main Functions
    ####################################################################################################################
    def generateQuizzes(self, numQuizzes, arrayOfRanges, outputFilename = "Quizzes.xlsx"):
        """
        Function to generate quizzes.

        Parameters:
            numQuizzes (int): The number of quizzes wanted.
            arrayOfRanges (array of str): Ranges to use for quiz generation.
            outputFilename (str): The name of the output file (Defaults to "Quizzes.xlsx").
        """

        # Error Checking
        if numQuizzes <= 0:
            print("Error!!! Invalid Number of Quizzes.")
            return
        elif not self.qL.mL.checkRange(arrayOfRanges):
            print("Error!!! Ranges are invalid.")
            return

        quizzes = [] # Array to store quizzes

        validQuestions = self.findValidQuestions(arrayOfRanges)
        usedQuestions = {"INT":[], "CR":[], "CVR":[], "MA":[], "Q":[], "FTV":[]}

        if self.qL.isGospel:
            usedQuestions["SIT"] = []

        quizNum = 0 # Iterator for number of quizzes
        while quizNum != numQuizzes:
            # Generate 25 quizzes to pick from
            quizSelection = []
            quizRatings = []
            i = 0
            while i != 50:
                quiz = self.generateQuiz(validQuestions, usedQuestions)
                rating = self.rateQuiz(quiz)

                quizSelection.append(quiz)
                quizRatings.append(rating)
                i += 1

            # Pick the quiz with the best score
            minIndex = quizRatings.index(min(quizRatings))
            finalQuiz = quizSelection[minIndex]

            # Add used questions
            for question in finalQuiz:
                if question in validQuestions[self.findMainType(question[4])]:
                    validQuestions[self.findMainType(question[4])].remove(question)
                if question not in usedQuestions[self.findMainType(question[4])]:
                    usedQuestions[self.findMainType(question[4])].append(question)

            quizzes.append(finalQuiz) # Add the quiz to the list of quizzes

            quizNum += 1 # Increment quiz number

        self.exportQuizzes(quizzes, outputFilename)

    ####################################################################################################################
    # Helper Functions
    ####################################################################################################################

    def generateQuiz(self, validQuestions, usedQuestions):
        # Generate a single Quiz
        tempValidQuestions = validQuestions.copy()
        tempUsedQuestions = usedQuestions.copy()
        quiz = []

        i = 0
        while i < self.numQuestions / 10:
            subQuiz = []
            subQuiz = self.fillMinimums(subQuiz, tempValidQuestions, tempUsedQuestions)
            subQuiz = self.fillRemainingNumbered(subQuiz, tempValidQuestions, tempUsedQuestions)
            random.shuffle(subQuiz)
            if not quiz:
                quiz = subQuiz
            else:
                quiz.extend(subQuiz)
            i += 1
        quiz = self.addAAndBQuestions(quiz, tempValidQuestions, tempUsedQuestions)
        return quiz

    def findValidQuestions(self, arrayOfRanges):
        """
        Function to find all valid questions in a given range.

        Parameters:
            arrayOfRanges (array of str): Ranges to search for questions in.

        Returns:
            validQuestions (dict): All valid questions within the range.
        """

        validQuestions = {"INT":[], "CR":[], "CVR":[], "MA":[], "Q":[], "FTV":[]}

        if self.qL.isGospel:
            validQuestions["SIT"] = []

        for question in self.qL.questionDatabase:
            searchVerse = ",".join([question[0], question[1], question[2]])
            if not self.qL.mL.isVerseInRange(searchVerse, arrayOfRanges):
                continue

            qMainType = self.findMainType(question[4])
            if not qMainType:
                print(question[4])
            validQuestions[qMainType].append(question)

        return validQuestions

    def findMainType(self, questionType):
        """
        Function to find main type based on input.

        Parameters:
            questionType (str): The type to look for.

        Returns:
            qMainType (str): The main type of inputted type.
        """

        searchTypes = \
            {"INT":["INT", "INTF"],
             "CR":["CR", "CRMA"],
             "CVR":["CVR", "CVRMA"],
             "MA":["MA"],
             "Q":["Q", "Q2"],
             "FTV":["FTV", "FT2V", "F2V", "FT", "FTN"],
             "SIT":["SIT"]}

        for qMainType in searchTypes.keys():
            for qType in searchTypes[qMainType]:
                if questionType.lower().find(qType.lower()) != -1:
                    return qMainType

    def fillMinimums(self, quiz, validQuestions, usedQuestions):
        """
        Function to fill the non INT questions to quiz.

        Parameters:
            quiz (array of questions): The entire quiz object.
            validQuestions (dict of arrays of questions): All valid questions for the reference range.
            usedQuestions (dict of arrays of questions): All used questions.

        Returns:
            quiz (array of questions): The entire quiz object.
        """

        qTypes = ["CR", "CVR", "MA", "Q", "FTV"]
        if self.qL.isGospel:
            qTypes.append("SIT")
        for qType in qTypes:
            if validQuestions[qType]:
                randomQuestion = random.choice(validQuestions[qType])
                if randomQuestion not in quiz:
                    quiz.append(randomQuestion)
                    validQuestions[qType].remove(randomQuestion)
                    usedQuestions[qType].append(randomQuestion)
                    continue

            if usedQuestions[qType]:
                randomQuestion = random.choice(usedQuestions[qType])
                quiz.append(randomQuestion)

        return quiz

    def fillRemainingNumbered(self, quiz, validQuestions, usedQuestions):
        """
        Function to fill remaining numbered questions to quiz.

        Parameters:
            quiz (array of questions): The entire quiz object.
            validQuestions (dict of arrays of questions): All valid questions for the reference range.
            usedQuestions (dict of arrays of questions): All used questions.

        Returns:
            quiz (array of questions): The entire quiz object.
        """

        while len(quiz) <= 9:
            if validQuestions["INT"]:
                randomQuestion = random.choice(validQuestions["INT"])
                if randomQuestion not in quiz:
                    quiz.append(randomQuestion)
                    validQuestions["INT"].remove(randomQuestion)
                    usedQuestions["INT"].append(randomQuestion)
                    continue
            if usedQuestions["INT"]:
                randomQuestion = random.choice(usedQuestions["INT"])
                quiz.append(randomQuestion)
                continue

        return quiz

    def addAAndBQuestions(self, quiz, validQuestions, usedQuestions):
        """
        Function to add A and B questions to quiz.

        Parameters:
            quiz (array of questions): The entire quiz object.
            validQuestions (dict of arrays of questions): All valid questions for the reference range.
            usedQuestions (dict of arrays of questions): All used questions.

        Returns:
            quiz (array of questions): The entire quiz object.
        """

        if self.numQuestions == 30:
            questionIndex = 25
        else:
            questionIndex = 15

        # Dict to track the number of question types used
        questionTypesUsed = {"INT": 0, "MA": 0, "CR": 0, "CVR": 0, "Q": 0, "FTV": 0}

        # Check to see if year is a gospel
        if self.qL.isGospel:
            questionTypesUsed["SIT"] = 0

        while questionIndex != self.numQuestions + 10:
            for i in range(2):
                questionPicked = False
                while not questionPicked:

                    # Pick a random type
                    randomQType = random.choice(list(questionTypesUsed.keys()))

                    # Check to see if question type has met it's maximum
                    if randomQType != "INT" and questionTypesUsed[randomQType] == 2:
                        del questionTypesUsed[randomQType]
                        continue
                    elif randomQType == "INT" and questionTypesUsed[randomQType] == 4:
                        del questionTypesUsed[randomQType]
                        continue
                    else:
                        if validQuestions[randomQType]:
                            randomQuestion = random.choice(validQuestions[randomQType])
                            # if randomQuestion not in quiz:
                            quiz.insert(questionIndex + i + 1, randomQuestion)
                            validQuestions[randomQType].remove(randomQuestion)
                            questionPicked = True
                        elif usedQuestions[randomQType]:
                            randomQuestion = random.choice(usedQuestions[randomQType])
                            #if randomQuestion not in quiz:
                            quiz.insert(questionIndex + i + 1, randomQuestion)
                            questionPicked = True

                questionTypesUsed[randomQType] = + 1

            questionIndex += 3
        return quiz

    def rateQuiz(self, quiz):
        """
        Function to assign a rating to a quiz.

        Parameters:
             quiz (array of questions): The quiz to be rated.

        Returns:
            score (int): The score of the given quiz.
        """

        score = 0
        previousType = ""
        usedChapters = []
        usedVerses = []

        for question in quiz:
            currentType = self.findMainType(question[4])
            if currentType == previousType:
                score += 1
            previousType = currentType

            chapter = str(question[0]) + str(question[1])
            verse = str(question[0]) + str(question[1]) + str(question[2])

            if verse in usedVerses:
                score += 5
            else:
                usedVerses.append(verse)

            if chapter in usedChapters:
                score += 1
            else:
                usedChapters.append(chapter)
        return score

    def exportQuizzes(self, quizzes, outputFilename):
        """
        Function to export quizzes to excel file.

        Parameters:
           quizzes (array of quiz objects): All of the quizzes to be outputted.
           outputFilename (str): The name of the output file.
        """

        if outputFilename == "Quizzes.xlsx":
            date = time.strftime("%Y_%m_%d")
            fileName = Path("../" + date + "_Quizzes.xlsx")
            workbook = xlsxwriter.Workbook(fileName)
        else:
            date = time.strftime("%Y_%m_%d")
            fileName = Path(str(Path.home()) + "/Documents/" + date + "_" + outputFilename + "_Quizzes.xlsx")
            workbook = xlsxwriter.Workbook(fileName)

        # Set formats
        qAndACellFormat = workbook.add_format({'text_wrap': 1, 'valign': 'top', 'border': 1})
        restCellFormat = workbook.add_format({'valign': 'top', 'border': 1})
        bold = workbook.add_format({'bold': 1})

        worksheet = workbook.add_worksheet("Quizzes")
        if self.numQuestions == 30:
            questionNumbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                           "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "26A", "26B", "27", "27A",
                           "27B", "28", "28A", "28B", "29", "29A", "29B", "30", "30A", "30B"]
        else:
            questionNumbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                           "16A", "16B", "17", "17A", "17B", "18", "18A", "18B", "19", "19A", "19B", "20", "20A", "20B"]



        # Size columns
        colLengthList = [3, 10, 32, 46, 4, 2, 2] # Lengths of columns in output file
        for i, width in enumerate(colLengthList):
            worksheet.set_column(i, i, width)

        i = 1
        for quizNum, quiz in enumerate(quizzes, start = 1):
            i += 1
            worksheet.write("A" + str(i), "Quiz " + str(quizNum))
            i += 1

            for questionIndex, question in enumerate(quiz):
                worksheet.write("A" + str(i), questionNumbers[questionIndex], restCellFormat)
                worksheet.write("B" + str(i), question[4], qAndACellFormat)
                worksheet.write_rich_string("C" + str(i), *self.boldUniqueWords(question[5], bold), qAndACellFormat)
                worksheet.write_rich_string("D" + str(i), *self.boldUniqueWords(question[6], bold), qAndACellFormat)
                worksheet.write("E" + str(i), question[0], restCellFormat)
                worksheet.write("F" + str(i), question[1], restCellFormat)
                worksheet.write("G" + str(i), question[2], restCellFormat)
                i += 1

        workbook.close()

    def boldUniqueWords(self, myString, boldFormat):
        """
        Function to bold unique words in a particular string.

        Parameters:
            myString (str): The input string to be bolded.
            boldFormat (xlsxwriter format object): The format to be applied to unique words.

        Returns:
            result (array) Array of strings and xlsxwriter objects.
        """

        # Check to make sure string is not a reference question or a quote
        rMatch = re.search(r'According\sto.*Chapter', myString, re.IGNORECASE)
        qMatch = re.search(r'Quote\sto.*Chapter', myString, re.IGNORECASE)
        if rMatch or qMatch:
            return [myString]

        result = []
        start = 0
        splitVerse = self.qL.mL.splitVerse(myString)
        for word in splitVerse:
            if word[0].lower() in self.qL.mL.uniqueWords:
                result.append(myString[start:word[1]])
                result.append(boldFormat)
                result.append(myString[word[1]:word[1] + len(word[0])])
                start = len(word[0]) + word[1]
        if start != len(myString):
            result.append(myString[start:])
        return result


if __name__ == "__main__":
    qM = QuizMaker()
    qM.numQuestions = 20
    refRange = ["John,13,1-John,14,14"]
    start_time = time.time()
    qM.generateQuizzes(5, refRange)
    print("Done in {:.2f}s".format(time.time() - start_time))
