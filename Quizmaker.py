###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
###################################################################################################

class Question:
    """
    A class to store the attributes of a question.

    Attributes:
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

        self.questionCode = qCode
        self.questionBook = qBook
        self.questionChapter = qChapter
        self.questionVerseStart = qVerseStart
        self.questionVerseEnd = qVerseEnd
        self.questionType = qType
        self.questionQuestion = qQuestion
        self.questionAnswer = qAnswer


class Chapter:
    """
    A class to store the attributes of a chapter of references.

    Attributes:
        chapterBook (str): The book of chapter.
        chapterChapter (str): The chapter of chapter.
        chapterVerses (array of str): The verses of chapter
    """

    def __init__(self, cBook, cChapter):
        """
        The constructor for class Chapter.

        Parameters:
            cBook(str): The book of chapter.
            cChapter(str): The chapter of chapter.
        """

        self.chapterBook = cBook
        self.chapterChapter = cChapter
        self.chapterVerses = []


class QuestionList:
    """
    A class to store the questions and perform functions on them.

    Attributes:
        questionDatabase (array of Question): The array that stores all of the questions.
    """

    questionDatabase = [] # The array that stores all of the material chapters

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

        questionFile = open(questionFileName, "r", encoding = "latin-1") # Open the file for reading
        #next(questionFile) # CDL=> Should we assume there is a header row?

        # For each line in file, place into proper question object
        for question in questionFile:
            fields = question.split("$")
            if fields[0] != "":
                fields[0] = self.alphaCodeToDigitCode(fields[0])
            questionObj = Question(fields[0], fields[1], fields[2],
                                   fields[3], fields[4], fields[5], fields[6], fields[7])
            self.questionDatabase.append(questionObj)
        questionFile.close() # Close the file
        self.generateCodes() # Add unique codes to those that do not have them
    
    def exportQuestions(self, questionFileName):
        """
        Function to export questions from QuestionList object.

        Parameters:
            questionFileName (str): The input filename for questions.
        """

        questionFile = open(questionFileName, "w", encoding = "latin-1")  # Open the file for writing

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
            questionFile.write(line)
        questionFile.close() # Close the file

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


class MaterialList:
    """
    A class to store the material and perform operations on it.

    Attributes:
        materialRange (array of Chapter objects): An array to store the material references data.
    """

    materialRange = [] # An array to store the material references data

    def __init__(self, materialFileName = "material.csv"):
        """
        The constructor for class MaterialList.

        Parameters:
            materialFileName (str): The input filename for material, defaults to "material.csv".
        """

        self.importMaterial(materialFileName)

    def importMaterial(self, materialFileName):
        """
        Function to import and store material.

        Parameters:
           materialFileName (str): The input filename for material.
        """

        materialFile = open(materialFileName, "r", encoding = "latin-1") # Open the file for reading

        # For each line in file, place into proper Chapter object
        for chapter in materialFile:
            chapter = chapter.rstrip()
            fields = chapter.split(",")
            materialObj = Chapter(fields[0], fields[1])
            for verse in fields[2:]:
                materialObj.chapterVerses.append(verse)
            self.materialRange.append(materialObj)
        materialFile.close() # Close the file

    def printMaterial(self):
        """
        Function print material.
        """

        for chapter in self.materialRange:
            verses = ",".join(chapter.chapterVerses)
            print(chapter.chapterBook + " " + chapter.chapterChapter + ": " + verses)

    def checkRange(self, arrayOfRanges):
        """
        Function to validate multiple ranges.

        Parameters:
            arrayOfRanges (array of str): Input ranges to be validated.

        Returns:
            (bool): True or False output indicating result of check
        """

        for refRange in arrayOfRanges:

            # Check to make sure all references are valid
            refRange = refRange.split("-")
            startRef = refRange[0].split(",")
            endRef = refRange[1].split(",")
            if not self.checkRef(startRef):
                return False
            if not self.checkRef(endRef):
                return False

            # Check to make sure all ranges are valid
            i = 0
            for chapter in self.materialRange:
                if startRef[0] == chapter.chapterBook and startRef[1] == chapter.chapterChapter:
                    startIndex = i

                if endRef[0] == chapter.chapterBook and endRef[1] == chapter.chapterChapter:
                    endIndex = i
                i += 1
            if startIndex > endIndex:
                return False

            elif startIndex == endIndex:
                if int(startRef[2]) > int(endRef[2]):
                    return False

        return True # Return True if ranges are not invalid

    def checkRef(self, reference):
        """
        Function to validate a reference.

        Parameters:
            reference (array of str): Input reference to be validated.

        Returns:
            (bool): True or False output indicating result of check
        """

        for chapter in self.materialRange:
            if reference[0] == chapter.chapterBook and reference[1] == chapter.chapterChapter:
                for verse in chapter.chapterVerses:
                    if verse == reference[2]:
                        return True
        return False


if __name__ == "__main__":

    # Example help functions
    # help(Question)
    # help(Chapter)
    # help(QuestionList)
    # help(MaterialList)

    ql1 = QuestionList() # Create an object of type QuestionList
    ml1 = MaterialList() # Create an object of type QuestionList

    # refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"] # Test range for checkRange func
    # print("Range Valid: " + str(ml1.checkRange(refRange))) # Testing checkRange func
    # ml1.printMaterial()  # Print the Material list to ensure it is working


# Extra functions and data for later

# configFilename = "config.csv"

#def importQuizConfig(self, configFilename)
#    configFile = open(configFilename, "r", encoding = "latin-1")
#    for line in configFile:
#        line.rstrip()
#    configFile.close()