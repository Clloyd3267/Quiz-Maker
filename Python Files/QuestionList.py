###################################################################################################
# Name        : QuestionList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage questions
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation

class Question:
    """
    A class to store the attributes of a question.

    Attributes:
        questionNumber (str): Used to store a question number.
        questionCode (int / str): The unique code of question.
        questionBook (str): The book of question.
        questionChapter (str): The chapter of question.
        questionVerseStart (str): The start verse of question.
        questionVerseEnd (str): The end verse (if any) of question.
        questionType (str): The type of question.
        questionQuestion (str): the question of question.
        questionAnswer (str): The answer to question.
    """

    def __init__(self, qCode, qBook, qChapter, qVerseStart, qVerseEnd, qType, qQuestion, qAnswer):
        """
        The constructor for class Question.

        Parameters:
            qCode (int / str): The unique code of question.
            qBook (str): The book of question.
            qChapter (str): The chapter of question.
            qVerseStart (str): The start verse of question.
            qVerseEnd (str): The end verse (if any) of question.
            qType (str): The type of question.
            qQuestion (str): the question of question.
            qAnswer (str): The answer to question.
        """

        self.questionNumber = ""
        self.questionCode = qCode
        self.questionBook = qBook
        self.questionChapter = qChapter
        self.questionVerseStart = qVerseStart
        self.questionVerseEnd = qVerseEnd
        self.questionType = qType
        self.questionQuestion = qQuestion
        self.questionAnswer = qAnswer

class QuestionList:
    """
    A class to store the questions and perform functions on them.

    Attributes:
        questionDatabase (array of Question): The array that stores all of the questions.
        isGospel (bool): Variable to store whether year is a gospel or not.
    """

    questionDatabase = []  # The array that stores all of the questions
    isGospel = 0  # Variable to store whether year is a gospel or not

    def __init__(self, questionFileName = "questions.txt"):
        """
        The constructor for class Question List.

        Parameters:
            questionFileName (str): The input filename for questions, defaults to "questions.txt".
        """

        self.importQuestions(questionFileName)
        self.exportQuestions(questionFileName)

    def importQuestions(self, questionFileName):
        """
        Function to import questions and populate QuestionList object.

        Parameters:
            questionFileName (str): The input filename for questions.
        """

        dataFilePath = Path("../Data Files/") # Path where datafiles are stored
        questionFile = open(dataFilePath / questionFileName, "r", encoding = 'UTF-8')
        # next(questionFile) # CDL=> Should we assume there is a header row?

        # For each line in file, place into proper question object
        for question in questionFile:
            question = question.rstrip()
            fields = question.split("$")
            if len(fields) != 8:
                print("Oops")
                continue
            if fields[0] != "":
                fields[0] = self.alphaCodeToDigitCode(fields[0])
            if "-" in fields[3]:
                verseRange = fields[3].split("-")
                fields[3] = verseRange[0]
                fields[4] = verseRange[1]
            if "sit" in fields[5].lower():
                self.isGospel = 1
            questionObj = Question(fields[0], fields[1], fields[2],
                                   fields[3], fields[4], fields[5], fields[6], fields[7])
            self.questionDatabase.append(questionObj)
        questionFile.close()
        self.generateCodes()  # Add unique codes to those that do not have them

    def exportQuestions(self, questionFileName):
        """
        Function to export questions from QuestionList object.

        Parameters:
            questionFileName (str): The output filename for questions.
        """

        dataFilePath = Path("../Data Files/") # Path where datafiles are stored
        questionFile = open(dataFilePath / questionFileName, "w", encoding = 'UTF-8')  # Open the file for writing

        # For each question in question list, write back out to file
        for question in self.questionDatabase:
            line = self.digitCodeToAlphaCode(question.questionCode) + "$"
            line += question.questionBook + "$"
            line += question.questionChapter + "$"
            line += question.questionVerseStart + "$"
            line += question.questionVerseEnd + "$"
            line += question.questionType + "$"
            line += question.questionQuestion + "$"
            line += question.questionAnswer
            line += "\n"
            questionFile.write(line)
        questionFile.close()

    def generateCodes(self):
        """
        Function to generate codes for questions that do not have codes.
        """

        # Find the highest code used
        largestCode = -1
        for question in self.questionDatabase:
            if question.questionCode != "":
                if largestCode < question.questionCode:
                    largestCode = question.questionCode

        # Increment largestCode
        if largestCode == -1:
            largestCode = 0
        else:
            largestCode = self.incrementCode(largestCode)

        # Assign codes to any questions that do not have one yet
        for question in self.questionDatabase:
            if question.questionCode == "":
                question.questionCode = largestCode
                largestCode = self.incrementCode(largestCode)

    def decToBin(self, decNum, numberOfBits):
        """
        Helper func that takes as an input a decimal number and converts it to a binary number.

        Parameters:
            decNum (int): Decimal number to be converted.
            numberOfBits (int): Number of bits that output number should be.

        Returns:
            binNum (str): The result of conversion.
        """

        decNum = int(decNum)
        formatCode = '0' + str(numberOfBits) + 'b'
        binNum = format(decNum, formatCode)
        return binNum

    def binToDec(self, binNum):
        """
        Helper func that takes as an input a binary number and converts it to a decimal number.

        Parameters:
            binNum (str): Binary number to be converted.

        Returns:
            decNum (int): The result of conversion.
        """

        binNum = str(binNum)
        decNum = int(binNum, 2)
        return decNum

    def alphaCodeToDigitCode(self, alphaCode):
        """
        Function to convert from "AAA" alpha code to a decimal number.

        Parameters:
           alphaCode (str): Three letter code to be converted.

        Returns:
            digitCode (int): The result of conversion.
        """

        asciiNums = [(ord(c) - 97) for c in alphaCode]
        binaryCode = (str(self.decToBin(asciiNums[0], 5)) +
                      str(self.decToBin(asciiNums[1], 5)) + str(self.decToBin(asciiNums[2], 5)))
        digitCode = self.binToDec(binaryCode)
        return digitCode

    def digitCodeToAlphaCode(self, digitCode):
        """
        Function to convert from decimal number to an "AAA" alpha code.

        Parameters:
           digitCode (int): Integer number to be converted.

        Returns:
            alphaCode (str): The result of conversion.
        """

        binaryCode = self.decToBin(digitCode, 15)
        separateBinNums = [binaryCode[0:5], binaryCode[5:10], binaryCode[10:15]]
        separateDecNums = [self.binToDec(separateBinNums[0]),
                           self.binToDec(separateBinNums[1]), self.binToDec(separateBinNums[2])]
        alphaCode = (str(chr(separateDecNums[0] + 97)) +
                     str(chr(separateDecNums[1] + 97)) + str(chr(separateDecNums[2] + 97)))
        return alphaCode

    def incrementCode(self, digitCode):
        """
        Function to increment custom integer code.

        Parameters:
           digitCode (int): Integer number to be incremented.

        Returns:
            digitCode (int): Integer number after being incremented.
        """

        # Convert to three decimal numbers 1-26
        binaryCode = self.decToBin(digitCode, 15)
        separateBinNums = [binaryCode[0:5], binaryCode[5:10], binaryCode[10:15]]
        separateDecNums = [self.binToDec(separateBinNums[0]),
                           self.binToDec(separateBinNums[1]), self.binToDec(separateBinNums[2])]

        # Increment Number
        if separateDecNums[2] < 25:
            separateDecNums[2] += 1

        elif separateDecNums[1] < 25:
            separateDecNums[1] += 1
            separateDecNums[2] = 0

        elif separateDecNums[0] < 25:
            separateDecNums[0] += 1
            separateDecNums[1] = 0
            separateDecNums[2] = 0
        else:
            print("ERROR!!! -> Code index went past 17576!")

        # Convert back to decimal
        binaryCode = (str(self.decToBin(separateDecNums[0], 5)) +
                      str(self.decToBin(separateDecNums[1], 5)) + str(self.decToBin(separateDecNums[2], 5)))
        digitCode = self.binToDec(binaryCode)
        return digitCode
    # CDL=> Add print function