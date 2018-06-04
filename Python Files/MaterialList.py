###################################################################################################
# Name        : MaterialList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage material references
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import openpyxl # For reading in material

class MaterialList:
    """
    A class to store the material and perform operations on it.

    Attributes:
        materialRange (array of str): An array to store the material references data.
    """

    materialRange = [] # An array to store the material references data

    def __init__(self, materialFileName = "material.xlsx"):
        """
        The constructor for class MaterialList.

        Parameters:
            materialFileName (str): The input filename for material, defaults to "material.xlsx".
        """

        self.importMaterial(materialFileName)
        print("=> MaterialList Initialized")

    def importMaterial(self, materialFileName):
        """
        Function to import and store material.

        Parameters:
           materialFileName (str): The input filename for material.
        """

        dataFilePath = Path("../Data Files/")  # Path where datafiles are stored
        if materialFileName == "material.xlsx":
            materialFilePath = dataFilePath / materialFileName
        else:
            materialFilePath = materialFileName

        try:
            book = openpyxl.load_workbook(materialFilePath)  # Open the workbook holding the material
        except IOError:
            print("Error => Material file does not exist!!!")
            return

        sheet = book.worksheets[0]  # Open the first sheet

        # Loop through all chapters and store verses
        for chapterData in sheet.iter_rows(min_row = 1, min_col = 1):
            book = str(chapterData[0].value)
            chapter = str(chapterData[1].value).replace(" ", "")
            for verse in chapterData[2:]:
                self.materialRange.append([book, chapter, str(verse.value).replace(" ", "")])

    def isVerseInRange(self, searchVerse, arrayOfRanges):
        """
        Function to validate that a verse is in one of multiple ranges.

        Parameters:
            searchVerse (str): Input verse to be validated.
            arrayOfRanges (array of str): Input ranges.

        Returns:
            (bool): True or False output indicating result of check.
        """

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
            else:
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


# if __name__ == '__main__':
#     ml1 = MaterialList()  # Create an object of type MaterialList
#     ml1.printMaterial()   # Print all References
#     refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"] # Test range for checkRange func
#     verse = "2 Corinthians,2,3"
#     print("Range Valid: " + str(ml1.checkRange(refRange))) # Testing checkRange func
#     print("Verse Valid: " + str(ml1.isVerseInRange(verse, refRange))) # Testing checkRange func