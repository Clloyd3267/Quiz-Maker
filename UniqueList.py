###################################################################################################
# Name        : UniqueList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Class to store uniques words
###################################################################################################

class UniqueList:
    """
    A class to store UniqueList.

    Attributes:
        uniqueWords (array of str): An array to hold all of the unique words.
    """

    uniqueWords = [] # An array to hold all of the unique words

    def __init__(self, UniqueWordsFileName = "uniquewords.csv"):
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

        uniqueWordsFile = open(UniqueWordsFileName, "r")

        # For each verse in object append to materialRange
        for uniqueWord in uniqueWordsFile:
            uniqueWord = uniqueWord.rstrip()
            self.uniqueWords.append(uniqueWord)
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


# if __name__ == '__main__':
#     ul1 = UniqueList()  # Create an object of type MaterialList
#     print(ul1.isWordUnique("Thus "))
