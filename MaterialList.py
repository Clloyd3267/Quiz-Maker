###################################################################################################
# Name        : MaterialList.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage material references
###################################################################################################

#
# class Chapter:
#     """
#     A class to store the attributes of a chapter of references.
#
#     Attributes:
#         chapterBook (str): The book of chapter.
#         chapterChapter (str): The chapter of chapter.
#         chapterVerses (array of str): The verses of chapter.
#     """
#
#     def __init__(self, cBook, cChapter):
#         """
#         The constructor for class Chapter.
#
#         Parameters:
#             cBook (str): The book of chapter.
#             cChapter (str): The chapter of chapter.
#         """
#
#         self.chapterBook = cBook
#         self.chapterChapter = cChapter
#         self.chapterVerses = []


class MaterialList:
    """
    A class to store the material and perform operations on it.

    Attributes:
        materialRange (array of array of str): An array to store the material references data.
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
            for verse in fields[2:]:
                self.materialRange.append([fields[0], fields[1], verse])
        materialFile.close()

    def printMaterial(self):
        """
        Function to print material.
        """

        chapter = []
        chapter.append(self.materialRange[0][0])
        chapter.append(self.materialRange[0][1])
        for verse in self.materialRange:
            if verse[1] != chapter[1]:
                chapterVerses = ",".join(chapter[2:])
                print(verse[0] + " " + verse[1] + ": " + chapterVerses)
                chapter.clear()
                chapter.append(verse[0])
                chapter.append(verse[1])
                chapter.append(verse[2])
            else:
                chapter.append(verse[2])

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
            print("Error!!! verse not in range or verse doesnt exist") # CDL=> ERROR spot
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
            if verse[0] == reference[0] and verse[1] == reference[1] and verse[2] == reference[2]:
                return True
        return False


# if __name__ == '__main__':
#     ml1 = MaterialList()  # Create an object of type MaterialList
#     ml1.printMaterial()   # Print all References
#     refRange = ["1 Corinthians,1,1-2 Corinthians,1,1"] # Test range for checkRange func
#     verse = "2 Corinthians,2,3"
#     print("Range Valid: " + str(ml1.checkRange(refRange))) # Testing checkRange func
#     print("Verse Valid: " + str(ml1.isVerseInRange(verse, refRange))) # Testing checkRange func