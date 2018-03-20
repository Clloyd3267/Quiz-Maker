###################################################################################################
# Name        : MaterialList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage material references
###################################################################################################


class Chapter:
    """
    A class to store the attributes of a chapter of references.

    Attributes:
        chapterBook (str): The book of chapter.
        chapterChapter (str): The chapter of chapter.
        chapterVerses (array of str): The verses of chapter.
    """

    def __init__(self, cBook, cChapter):
        """
        The constructor for class Chapter.

        Parameters:
            cBook (str): The book of chapter.
            cChapter (str): The chapter of chapter.
        """

        self.chapterBook = cBook
        self.chapterChapter = cChapter
        self.chapterVerses = []


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

        materialFile = open(materialFileName, "r")

        # For each line in file, place into proper Chapter object
        for chapter in materialFile:
            chapter = chapter.rstrip()
            fields = chapter.split(",")
            materialObj = Chapter(fields[0], fields[1])
            for verse in fields[2:]:
                materialObj.chapterVerses.append(verse)
            self.materialRange.append(materialObj)
        materialFile.close()

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
            (bool): True or False output indicating result of check.
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
            (bool): True or False output indicating result of check.
        """

        for chapter in self.materialRange:
            if reference[0] == chapter.chapterBook and reference[1] == chapter.chapterChapter:
                for verse in chapter.chapterVerses:
                    if verse == reference[2]:
                        return True
        return False