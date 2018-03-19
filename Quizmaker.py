###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd
# Description : A program to create quizzes
###################################################################################################

class Question:
    def __init__(self, qCode, qBook, qChapter, qVerseStart, qVerseEnd, qType, qQuestion, qAnswer):
        self.questionCode = qCode
        self.questionBook = qBook
        self.questionChapter = qChapter
        self.questionVerseStart = qVerseStart
        self.questionVerseEnd = qVerseEnd
        self.questionType = qType
        self.questionQuestion = qQuestion
        self.questionAnswer = qAnswer

class Chapter:
    def __init__(self, cBook, cChapter):
        self.chapterBook = cBook
        self.chapterChapter = cChapter
        self.chapterVerses = []


class QuestionList:
    questionDatabase = []
    materialRange = []

    def __init__(self, configFilename = "config.csv", questionFileName="questions.txt", materialFileName = "material.csv"):
      self.importQuestions(questionFileName)
      self.importMaterial(materialFileName)
      self.exportQuestions(questionFileName)

    def importQuestions(self, questionFileName):
        questionFile = open(questionFileName, "r", encoding = "latin-1")
        #next(questionFile)
        for question in questionFile:
            # question = question.rstrip(",")
            fields = question.split("$")
            # if len(fields) != 8:
            #     print(str(i) + ": " + str(len(fields)))

            if fields[0] != "":
                fields[0] = self.alphaCodeToDigitCode(fields[0])
            questionObj = Question(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7])
            self.questionDatabase.append(questionObj)
        questionFile.close()
        self.generateCodes()

    def importMaterial(self, materialFileName):
        materialFile = open(materialFileName, "r", encoding = "latin-1")
        for chapter in materialFile:
            chapter = chapter.rstrip()
            fields = chapter.split(",")
            materialObj = Chapter(fields[0], fields[1])
            for verse in fields[2:]:
                materialObj.chapterVerses.append(verse)
            self.materialRange.append(materialObj)
        materialFile.close()
    
    def exportQuestions(self, questionFileName):
        # open(questionFileName,"w").close()
        questionFile = open(questionFileName, "w", encoding = "latin-1")
        for question in self.questionDatabase:
            line =  self.digitCodeToAlphaCode(question.questionCode) + "$"
            line += question.questionBook + "$"
            line += question.questionChapter + "$"
            line += question.questionVerseStart + "$"
            line += question.questionVerseEnd + "$"
            line += question.questionType + "$"
            line += question.questionQuestion + "$"
            line += question.questionAnswer
            questionFile.write(line)
        questionFile.close()

    #def importQuizConfig(self, configFilename)
    #    configFile = open(configFilename, "r", encoding = "latin-1")
    #    for line in configFile:
    #        line.rstrip()
    #    configFile.close()

    # def printQuestions(self):
    #   for question in self.questionDatabase:
    #     print("Type: " + question.Type + " Question: " + question.Question +
    #           " Answer: " + question.Answer + " Book: " + question.Book +
    #           " Chapter: " + question.Chapter + " Verse: " + question.Verse)

    def printMaterial(self):
        for chapter in self.materialRange:
            verses = ",".join(chapter.chapterVerses)
            print(chapter.chapterBook + " " + chapter.chapterChapter + ": " + verses)

    def generateCodes(self):
        """Function to generate codes for questions that do not have one yet"""
    
        # Find the highest code used
        largestCode = -1
        for question in self.questionDatabase:
            if question.questionCode != "":
                if largestCode < question.questionCode:
                    largestCode = question.questionCode

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
        """Helper func that takes as an input a decimal number and converts it to a binary number"""
    
        decNum = int(decNum)
        formatCode = '0' + str(numberOfBits) + 'b'
        binNum = format(decNum, formatCode)
        return binNum
    
    def binToDec(self, binNum):
        """Helper func that takes as an input a binary number and converts it to a decimal number"""
    
        binNum = str(binNum)
        decNum = int(binNum, 2)
        return decNum
    
    def alphaCodeToDigitCode(self, alphaCode):
        """Function to convert from "AAA" alpha code to a decimal number"""
    
        asciiNums = [(ord(c) - 97) for c in alphaCode]
        binaryCode = str(self.decToBin(asciiNums[0], 5)) + str(self.decToBin(asciiNums[1], 5)) + str(self.decToBin(asciiNums[2], 5))
        digitCode = self.binToDec(binaryCode)
        return digitCode
    
    def digitCodeToAlphaCode(self, digitCode):
        """Function to convert from decimal number to an "AAA" alpha code"""
    
        binaryCode = self.decToBin(digitCode, 15)
        separateBinNums = [binaryCode[0:5], binaryCode[5:10], binaryCode[10:15]]
        separateDecNums = [self.binToDec(separateBinNums[0]), self.binToDec(separateBinNums[1]), self.binToDec(separateBinNums[2])]
        alphaCode = str(chr(separateDecNums[0] + 97)) + str(chr(separateDecNums[1] + 97)) + str(chr(separateDecNums[2] + 97))
        return alphaCode

    def incrementCode(self, digitCode):

        # Convert to three decimal numbers 1-26
        binaryCode = self.decToBin(digitCode, 15)
        separateBinNums = [binaryCode[0:5], binaryCode[5:10], binaryCode[10:15]]
        separateDecNums = [self.binToDec(separateBinNums[0]), self.binToDec(separateBinNums[1]), self.binToDec(separateBinNums[2])]

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
        binaryCode = str(self.decToBin(separateDecNums[0], 5)) + str(self.decToBin(separateDecNums[1], 5)) + str(self.decToBin(separateDecNums[2], 5))
        digitCode = self.binToDec(binaryCode)
        return digitCode


ql1 = QuestionList()        