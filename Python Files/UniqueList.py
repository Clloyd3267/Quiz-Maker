###################################################################################################
# Name        : UniqueList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Class to store and manage uniques words
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation

class UniqueList:
    """
    A class to store UniqueList.

    Attributes:
        uniqueWords (array of str): An array to hold all of the unique words.
    """

    uniqueWords = [] # An array to hold all of the unique words
    partOfWord = [] # An array to hold any characters that are not a number or letter.


    def __init__(self, UniqueWordsFileName = "UniqueWords.txt"):
        """
        The constructor for class MaterialList.

        Parameters:
            UniqueWordsFileName (str): The input filename for Unique Words, defaults to "unique.csv".
        """

        self.importUniqueWords(UniqueWordsFileName)

    def importUniqueWords(self, UniqueWordsFileName):
        """
        Function to import and store Unique Words.

        Parameters:
           UniqueWordsFileName (str): The input filename for Unique Words.
        """

        dataFilePath = Path("../Data Files/") # Path where datafiles are stored
        uniqueWordsFile = open(dataFilePath / UniqueWordsFileName, "r", encoding = 'UTF-8')

        for uniqueWord in uniqueWordsFile:
            uniqueWord = uniqueWord.rstrip()
            if not uniqueWord:
                continue
            self.uniqueWords.append(uniqueWord)

            for character in uniqueWord:
                if character not in self.partOfWord and not character.isalnum() and not character.isspace():
                    self.partOfWord.append(character)

        uniqueWordsFile.close()

    def isWordUnique(self, testWord):
        """
        Function to import and store Unique Words.

        Parameters:
           testWord (str): The input word to be tested.

        Returns:
            True (bool): Word is unique.
            false (bool): Word is not unique.
        """

        testWord = testWord.replace(" ", "")
        testWord = testWord.lower()
        for uniqueWord in self.uniqueWords:
            uniqueWord = uniqueWord.replace(" ", "")
            uniqueWord = uniqueWord.lower()
            if testWord == uniqueWord:
                return True
        return False
