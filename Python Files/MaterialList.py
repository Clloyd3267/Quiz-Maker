###################################################################################################
# Name        : MaterialList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Class to store and manage material references
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import openpyxl # For reading in material

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MaterialList:
    """
    A class to store the material and perform operations on it.

    Attributes:
        allVerses (array of verse objects) An array to store all of the verses.
        materialRange (array of str): An array to store the material references data.
        uniqueWords (array of str): An array to hold all of the unique words.
    """

    allVerses = [] # An array to store all of the verses.
    materialRange = [] # An array to store the material references data
    uniqueWords = []  # An array to hold all of the unique words

    def __init__(self, versesFileName = "Verses.xlsx"):
        """
        The constructor for class MaterialList.

        Parameters:
            versesFileName (str): The input filename for material (Defaults to "Verses.xlsx").
        """

        self.importVerses(versesFileName)

    def importVerses(self, versesFileName):
        """
        Function to import verses from an Excel file.

        Parameters:
            versesFileName (str): The input filename for verse list.

        Returns:
            (0): No errors, (Anything else): Errors.
        """

        # Create the path for Verse file
        dataFilePath = Path("Data Files/")  # Path where datafiles are stored
        dataFilePath = resource_path(dataFilePath)

        if versesFileName == "Verses.xlsx":
            versesFilePath = Path(dataFilePath) / versesFileName
        else:
            versesFilePath = versesFileName

        # Try opening the verses file
        try:
            book = openpyxl.load_workbook(versesFilePath)
        except IOError:
            return "Error => Verses file does not exist!!!"

        sheet = book.worksheets[0]  # Open the first sheet

        # Read in and parse all verses
        for row in sheet.iter_rows(min_row = 2, min_col = 1, max_col = 4):
            # Check to make sure verse is valid
            verse = []
            valid = False

            for cell in row:
                if not cell.value:
                    verse.append("")
                else:
                    verse.append(str(cell.value).strip())
                    valid = True

            if not valid:
                continue
            if not verse[0]:
                return "Error => No Book!!! " + verse[0] + " " + verse[1] + ":" + verse[2] + " " + verse[3]
            if not verse[1]:
                return "Error => No Chapter!!! " + verse[0] + " " + verse[1] + ":" + verse[2] + " " + verse[3]
            if not verse[2]:
                return "Error => No Verse Number!!! " + verse[0] + " " + verse[1] + ":" + verse[2] + " " + verse[3]
            if not verse[3]:
                return "Error => No Verse!!! " + verse[0] + " " + verse[1] + ":" + verse[2] + " " + verse[3]

            # Split verse
            verse.append(self.splitVerse(verse[3]))

            # Add verse to list of all verse references
            self.materialRange.append([str(verse[0]), str(verse[1]), str(verse[2])])

            # Add verse to list of all verses
            self.allVerses.append(verse)

        # Create Unique Words
        self.createUniqueWords()

        return 0 # Return with no errors

    def createUniqueWords(self):
        """
        Function to create list of all Unique Words.

        Returns:
            (0): No errors, (Anything else): Errors.
        """

        tempConcordance = {}
        for verse in self.allVerses:
            for i, word in enumerate(verse[4]):
                newVerseText = verse[3][0:word[1]] + "◆" + verse[3][word[1] + len(word[0]):]
                word = str(word[0]).upper()

                if word in tempConcordance:
                    tempConcordance[word][1].append([verse[0], verse[1], verse[2], newVerseText])
                    tempConcordance[word][0] += 1
                else:
                    tempConcordance[word] = [1, [[verse[0], verse[1], verse[2], newVerseText]]]

        for word, value in sorted(tempConcordance.items()):
            firstOccurence = value[1][0][0:3]
            uniqueWord = True
            for occurence in value[1]:
                if occurence[0:3] != firstOccurence:
                    uniqueWord = False
            if uniqueWord:
                self.uniqueWords.append(word.lower())

        return 0  # Return with no errors

    def isVerseInRange(self, searchVerse, arrayOfRanges):
        """
        Function to validate that a verse is in one of multiple ranges.

        Parameters:
            searchVerse (str): Input verse to be validated.
            arrayOfRanges (array of str): Input ranges.

        Returns:
            (bool): True or False output indicating result of check.
        """

        # Validate inputs
        searchVerse = searchVerse.split(",")
        if not self.checkRange(arrayOfRanges) or not self.checkRef(searchVerse):
            print("Error => Verse not in range or verse doesn't exist!!!", searchVerse[0], searchVerse[1], searchVerse[2]) # CDL=> ERROR spot
            return False

        for refRange in arrayOfRanges:
            refRange = refRange.split("-")
            startRef = refRange[0].split(",")
            endRef = refRange[1].split(",")

            i = 0
            for verse in self.materialRange:
                if verse[0] == startRef[0] and verse[1] == startRef[1] and verse[2] == startRef[2]:
                    startIndex = i

                if verse[0] == searchVerse[0] and verse[1] == searchVerse[1] and verse[2] == searchVerse[2]:
                    searchVerseIndex = i

                if verse[0] == endRef[0] and verse[1] == endRef[1] and verse[2] == endRef[2]:
                    endIndex = i
                i += 1

            if startIndex <= searchVerseIndex <= endIndex:
                return True

        #  If verse not found in ranges
        return False

    def checkRange(self, arrayOfRanges):
        """
        Function to validate multiple ranges.

        Parameters:
            arrayOfRanges (array of str): Input ranges to be validated.

        Returns:
            (bool): True or False output indicating result of check.
        """

        for refRange in arrayOfRanges:

            # Check to make sure all references are valid
            refRange = refRange.split("-")
            startRef = refRange[0].split(",")
            endRef = refRange[1].split(",")
            if not self.checkRef(startRef) or not self.checkRef(endRef):
                return False

            i = 0
            for verse in self.materialRange:
                if verse[0] == startRef[0] and verse[1] == startRef[1] and verse[2] == startRef[2]:
                    startIndex = i

                if verse[0] == endRef[0] and verse[1] == endRef[1] and verse[2] == endRef[2]:
                    endIndex = i
                i += 1

            if startIndex > endIndex:
                return False
        return True

    def checkRef(self, reference):
        """
        Function to validate a reference.

        Parameters:
            reference (array of str): Input reference to be validated.

        Returns:
            (bool): True or False output indicating result of check.
        """

        for verse in self.materialRange:
            if verse[0] == str(reference[0]) and verse[1] == str(reference[1]) and verse[2] == str(reference[2]):
                return True
        return False

    def splitVerse(self, verseText):
        """
        Function to split a verse into individual words.

        Parameters:
            verseText(str): Text of verse to be split.

        Returns:
            splitVerse(arr): Array of array of str and int representing split verse text.
        """
        splitVerse = []
        partOfWord = ["", 0]

        # Loop through all characters with index
        for i, character in enumerate(verseText):
            # Character is part of word
            if (character.isalnum()) or \
            (character == "-") or \
            (character in ["’" , "'"] and partOfWord[0] != "" and
            (i != 0 and (verseText[i - 5:i].lower() == "jesus") or
            (i != len(verseText) - 1 and i != 0 and verseText[i - 1].isalnum() and verseText[i + 1].isalnum()))):
                if partOfWord[0] == "":
                    partOfWord[1] = i
                partOfWord[0] += character

            # Character is not part of word
            else:
                if partOfWord[0]:
                    splitVerse.append(partOfWord.copy())
                    partOfWord[0] = ""
                    partOfWord[1] = 0

        # Append any leftover characters to splitVerse
        if partOfWord[0]:
            splitVerse.append(partOfWord.copy())

        return splitVerse

    def isWordUnique(self, testWord):
        """
        Function to check if word is unique.

        Parameters:
           testWord (str): The input word to be tested.

        Returns:
            True (bool): Word is unique.
            False (bool): Word is not unique.
        """

        testWord = testWord.replace(" ", "")
        testWord = testWord.lower()
        if testWord in self.uniqueWords:
            return True
        else:
            return False
