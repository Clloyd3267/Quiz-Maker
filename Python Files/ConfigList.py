###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage config files
###################################################################################################

# External Imports
from pathlib import Path # Used for file manipulation
import os # Used for file manipulation


class Config:
    """
    A class to store config data.

    Attributes:
        configName (str): Name of configuration.
        numberOfQuestions (str): The number of questions for each quiz.
        isAAndB (str): Whether or not to have A's and B's.
        randAB (str): Whether or not A's and B's are random.
        sameAB (str): Whether or not A's and B's are the same as numbered question.
        intWeight (str): The weight of INTs for each quiz.
        typeMinMax (dict of arrays of str): Min and Max data for configuration. (see table below for more info)

    Structure of typeMinMax:
        MINMA,  MAXMA
        MINCR,  MAXCR
        MINCVR, MAXCVR
        MINQ,   MAXQ
        MINFTV, MAXFTV
        MINSIT, MAXSIT
    """

    def __init__(self, cConfigName, cNumberOfQuestions, cIsAAndB, cRandAB, cSameAB, cIntWeight, cTypeMinMax):
        """
        The constructor for class config.

        Parameters:
            cConfigName (str): Name of configuration.
            cNumberOfQuestions (str): The number of questions for each quiz.
            cIsAAndB (str): Whether or not to have A's and B's.
            cRandAB (str): Whether or not A's and B's are random.
            cSameAB (str): Whether or not A's and B's are the same as numbered question.
            cIntWeight (str): The weight of INTs for each quiz.
            cTypeMinMax (array of arrays of str): Min and Max data for configuration.
        """

        self.configName = cConfigName
        self.numberOfQuestions = cNumberOfQuestions
        self.isAAndB = cIsAAndB
        self.randAB = cRandAB
        self.sameAB = cSameAB
        self.intWeight = cIntWeight
        self.typeMinMax = cTypeMinMax


class ConfigList:
    """
    A class to store the config files and perform operations on it.

    Attributes:
        configList (array of config objects): An array to store the config data.
    """

    configList = {} # The dict of config data objects

    def __init__(self, configFileName = "QuizMakerConfig.csv"):
        """
        Constructor of class ConfigList.

        Parameters:
            ConfigFileName (str): Input file name of program config data.
        """

        self.importConfigFiles(configFileName)

    def importConfigFiles(self, configFileName):
        """
        Function to import config data.

        Parameters:
            configFileName (str): The input file name of program config data.
        """

        dataFilePath = Path("../Data Files/Config Files/") # Path where datafiles are stored
        configFileNames = ["default.csv"]  # The array that stores all of the config filenames

        # Ensure that the program config file exists, if not make it
        try:
            configFile = open(dataFilePath / configFileName, 'r')
        except IOError:
            configFile = open(dataFilePath / configFileName, 'w')
        configFile.close()

        # Read in filenames for config files
        configFile = open(dataFilePath / configFileName, "r")
        for line in configFile:
            line = line.rstrip()
            configFileNames.append(line)
        configFile.close()

        # Read in Config data from each file
        for fileName in configFileNames:
            file = open(dataFilePath / fileName, "r")
            numberOfQuestions = file.readline().rstrip()[18:]
            isAAndB = file.readline().rstrip()[8:]
            randAB = file.readline().rstrip()[7:]
            sameAB = file.readline().rstrip()[7:]
            intWeight = file.readline().rstrip()[10:]
            file.readline()
            typeMinsAndMaxs = {}
            while True:
                line = file.readline().rstrip()
                if not line:
                    break
                qType = line[0:line.find(":")]
                data = line[line.find(":") + 1:]
                typeMinsAndMaxs[qType] = data.split(",")
            self.configList[fileName[:-4]] = Config(fileName[:-4], numberOfQuestions, isAAndB,
                                                    randAB, sameAB, intWeight, typeMinsAndMaxs)
            file.close()

    def exportConfigFiles(self, configFileName = "QuizMakerConfig.csv"):
        """
        Function to export config data.

        Parameters:
            configFileName (str): The output file name of program config data.
        """

        # Write out filenames for config files
        dataFilePath = Path("../Data Files/Config Files/")  # Path where datafiles are stored

        configFile = open(dataFilePath / configFileName, "w")
        for configName in list(self.configList.keys()):
            fileName = configName + ".csv\n"
            if fileName != "default.csv\n":
                configFile.write(fileName)
                fileName = configName + ".csv"
                file = open(dataFilePath / fileName, 'w')
                file.write("numberOfQuestions:" + str(self.configList[configName].numberOfQuestions) + "\n")
                file.write("isAAndB:" + str(self.configList[configName].isAAndB) + "\n")
                file.write("randAB:" + str(self.configList[configName].randAB) + "\n")
                file.write("sameAB:" + str(self.configList[configName].sameAB) + "\n")
                file.write("intWeight:" + str(self.configList[configName].intWeight) + "\n")
                file.write("Min,Max\n")
                for qType in list(self.configList[configName].typeMinMax.keys()):
                    file.write(str(qType) + ":" + str(self.configList[configName].typeMinMax[qType][0]) + "," +
                               str(self.configList[configName].typeMinMax[qType][0]) + "\n")
                file.close()
        configFile.close()

    def addConfigFile(self, configData):
        """
        Function to add config data.

        Parameters:
            configData (Config): A config object to be added.
        """

        #     CDL=> Add validation
        self.configList[configData.configName] = configData
        self.exportConfigFiles()

    def deleteConfigFile(self, configName):
        """
        Function to delete config data.

        Parameters:
            configName (str): Name of config data to be deleted.
        """

        #     CDL=> Add validation
        dataFilePath = Path("../Data Files/Config Files/")  # Path where datafiles are stored

        del self.configList[configName]
        self.exportConfigFiles()
        fileName = configName + ".csv"
        os.remove(dataFilePath / fileName)

    # CDL=> Add addConfig and editConfig and exportConfigFiles functions
# if __name__ == "__main__":
    # c1 = Config("test","20","1","1","0","5",{"MA":["2","2"],
    #                                          "CR":["2","2"],
    #                                          "CVR":["2","2"],
    #                                          "Q":["2","2"],
    #                                          "FTV":["2","2"],
    #                                          "SIT":["2","2"]})
    # c2 = Config("yay", "20", "1", "1", "0", "5", {"MA": ["2", "2"],
    #                                                "CR": ["2", "2"],
    #                                                "CVR": ["2", "2"],
    #                                                "Q": ["2", "2"],
    #                                                "FTV": ["2", "2"],
    #                                                "SIT": ["2", "2"]})
    #
    # cL = ConfigList()  # Create an object of type ConfigList
    # # cL.addConfigFile(c1)
    # # cL.addConfigFile(c2)
    # cL.deleteConfigFile("yay")
