###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : Classes to store and manage config files
###################################################################################################


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

        configFileNames = ["default.csv"]  # The array that stores all of the config filenames

        # Ensure that the program config file exists, if not make it
        try:
            configFile = open(configFileName, 'r')
        except IOError:
            configFile = open(configFileName, 'w')
        configFile.close()

        # Read in filenames for config files
        configFile = open(configFileName, "r")
        for line in configFile:
            line.rstrip()
            configFileNames.append(line)
        configFile.close()

        # Read in Config data from each file
        for fileName in configFileNames:
            file = open(fileName, "r")
            line1 = (file.readline()).rstrip()
            line1 = line1.split(",")
            typeMinsAndMaxs = {}
            questionTypes = ["MA", "CR", "CVR", "Q", "FTV", "SIT"]
            i = 0
            for line in file:
                line = line.rstrip()
                typeMinsAndMaxs[questionTypes[i]] = line.split(",")
                i += 1
            self.configList[fileName[:-4]] = Config(fileName[:-4], line1[0], line1[1],
                                                    line1[2], line1[3], line1[4], typeMinsAndMaxs)
            file.close()

    def printConfigData(self):
        """
        Function to print config data.
        """

        for config in self.configList:
            print("=====================================")
            print("Config Data for: " + self.configList[config].configName)
            print("Number of Questions: " + self.configList[config].numberOfQuestions)
            print("Are there A's and B's: " + self.configList[config].isAAndB)
            if self.configList[config].randAB == "1" and self.configList[config].sameAB == "0":
                aBType = "Random"
            elif self.configList[config].sameAB == "1" and self.configList[config].randAB == "0":
                aBType = "Same as numbered question"
            print("INT weight: " + str(self.configList[config].intWeight))
            print("A's and B's question type: " + aBType)
            print("    Min, Max")
            print("Ma:  " + self.configList[config].typeMinMax[0][0] + ",   " + self.configList[config].typeMinMax[0][1])
            print("CR:  " + self.configList[config].typeMinMax[1][0] + ",   " + self.configList[config].typeMinMax[1][1])
            print("CVR: " + self.configList[config].typeMinMax[2][0] + ",   " + self.configList[config].typeMinMax[2][1])
            print("Q:   " + self.configList[config].typeMinMax[3][0] + ",   " + self.configList[config].typeMinMax[3][1])
            print("FTV: " + self.configList[config].typeMinMax[4][0] + ",   " + self.configList[config].typeMinMax[4][1])
            print("SIT: " + self.configList[config].typeMinMax[5][0] + ",   " + self.configList[config].typeMinMax[5][1])
            print("=====================================")
    # def exportConfigFiles(self, configFileName):
    #     """
    #     Function to export config data.
    #
    #     Parameters:
    #         configFileName (str): The output file name of program config data.
    #     """
    # CDL=> Add addConfig and editConfig and exportConfigFiles functions