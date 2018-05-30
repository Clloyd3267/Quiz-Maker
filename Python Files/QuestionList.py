###################################################################################################
# Name        : QuestionList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage questions
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import openpyxl # For reading in questions

# Project Imports
from MaterialList import * # Used to check the reference of questions

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
        mL (MaterialList): Used for checking the references.
        importErrors (array of errors): Errors while importing.
        questionDatabase (array of Question): The array that stores all of the questions.
        isGospel (bool): Variable to store whether year is a gospel or not.
    """

    mL = MaterialList() # Object of type MaterialList
    importErrors = [] # Errors while importing
    questionDatabase = []  # The array that stores all of the questions
    isGospel = 0  # Variable to store whether year is a gospel or not

    def __init__(self, questionFileName = "questions.xlsx"):
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

        dataFilePath = Path("../Data Files/")  # Path where datafiles are stored
        if questionFileName == "questions.xlsx":
            questionFilePath = dataFilePath / questionFileName
        else:
            questionFilePath = questionFileName

        try:
            book = openpyxl.load_workbook(questionFilePath)
        except IOError:
            print("Error => Question file does not exist!!!")
            return

        sheet = book.active  # Open the active sheet
        for row in sheet.iter_rows(min_row = 1, min_col = 1, max_col = 8):
            question = []
            for cell in row:
                if not cell.value:
                    question.append("")
                else:
                    question.append(str(cell.value))

            # Check question code
            valid = False
            if question[0]:
                if len(question[0]) == 3:
                    if question[0][0].isalpha() and question[0][1].isalpha() and question[0][2].isalpha():
                        valid = True
            else:
                valid = True

            if not valid:
                self.importErrors.append(["Error => Question code invalid!!!", question[:8]])
                continue

            # Check reference
            if not question[1]:
                self.importErrors.append(["Error => No book!!!", question[:8]])
                continue
            if not question[2]:
                self.importErrors.append(["Error => No chapter!!!", question[:8]])
                continue
            if not question[3]:
                self.importErrors.append(["Error => No verse start!!!", question[:8]])
                continue
            if not self.mL.checkRef([question[1],question[2],question[3]]):
                self.importErrors.append(["Error => Verse start invalid!!!", question[:8]])
                continue
            if question[4] and not self.mL.checkRef([question[1], question[2], question[4]]):
                self.importErrors.append(["Error => Verse end invalid!!!", question[:8]])
                continue

            # Check type
            searchTypes = \
                {"INT": ["INT", "INTF"],
                 "CR": ["CR", "CRMA"],
                 "CVR": ["CVR", "CVRMA"],
                 "MA": ["MA"],
                 "Q": ["Q", "Q2"],
                 "FTV": ["FTV", "FT2V", "F2V", "FT", "FTN"]}
            valid = False
            for qMainType in searchTypes.keys():
                for qType in searchTypes[qMainType]:
                    if question[5].lower().find(qType.lower()) != -1:
                        valid = True
            if not valid:
                self.importErrors.append(["Error => Question type invalid!!!", question[:8]])
                continue

            # Check question and answer
            if not question[6]:
                self.importErrors.append(["Error => No question!!!", question[:8]])
                continue
            if not question[7]:
                self.importErrors.append(["Error => No answer!!!", question[:8]])
                continue

            # Convert letter question code to number code
            if question[0] != "":
                question[0] = self.alphaCodeToDigitCode(question[0])

            # check for Gospel
            if "sit" in question[5].lower():
                self.isGospel = 1

            questionObj = Question(question[0], question[1], question[2],
                                   question[3], question[4], question[5], question[6], question[7])
            self.questionDatabase.append(questionObj)
        self.generateCodes()  # Add unique codes to those that do not have them
        self.printImportErrors()

    def exportQuestions(self, questionFileName):
        """
        Function to export questions from QuestionList object.

        Parameters:
            questionFileName (str): The output filename for questions.
        """

        dataFilePath = Path("../Data Files/")  # Path where datafiles are stored
        if questionFileName == "questions.xlsx":
            questionFilePath = dataFilePath / questionFileName
        else:
            questionFilePath = questionFileName

        try:
            book = openpyxl.load_workbook(questionFilePath)
        except IOError:
            print("Error => Question file does not exist!!!")
            return
        sheet1 = book.active  # Open the active sheet questionFileName
        book.remove(sheet1)
        for i in book.worksheets:
            if i.title == "Errors":
                book.remove(i)
            elif i.title == "Questions":
                book.remove(i)
        book.create_sheet("Questions")
        book.create_sheet("Errors")
        sheet1 = book["Questions"]
        sheet2 = book["Errors"]

        for rowNum, question in enumerate(self.questionDatabase, start = 1):
            sheet1.cell(row = rowNum, column = 1).value = self.digitCodeToAlphaCode(question.questionCode)
            sheet1.cell(row = rowNum, column = 2).value = question.questionBook
            sheet1.cell(row = rowNum, column = 3).value = question.questionChapter
            sheet1.cell(row = rowNum, column = 4).value = question.questionVerseStart
            sheet1.cell(row = rowNum, column = 5).value = question.questionVerseEnd
            sheet1.cell(row = rowNum, column = 6).value = question.questionType
            sheet1.cell(row = rowNum, column = 7).value = question.questionQuestion
            sheet1.cell(row = rowNum, column = 8).value = question.questionAnswer

        for rowNum, questionError in enumerate(self.importErrors, start = 1):
            i = 1
            while i != 9:
                sheet2.cell(row = rowNum, column = i).value = questionError[1][i - 1]
                i += 1
            sheet2.cell(row = rowNum, column = 9).value = questionError[0]

        book.save(dataFilePath / questionFileName)

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

    def printImportErrors(self):
        """
        Function to print errors.
        """
        for error in self.importErrors:
            print("->", error[0])
            print("  ", error[1])
