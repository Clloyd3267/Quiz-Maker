###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd, Andrew Southwick
# Description : A program to create quizzes
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
        typeMinMax (array of arrays of str): Min and Max data for configuration. (see table below for more info)

    Structure of typeMinMax:
        MINMA,  MAXMA
        MINCR,  MAXCR
        MINCVR, MAXCVR
        MINQ,   MAXQ
        MINFTV, MAXFTV
        MINSIT, MAXSIT
    """

    def __init__(self, cConfigName, cNumberOfQuestions, cIsAAndB, cRandAB, cSameAB, cTypeMinMax):
        """
        The constructor for class config.

        Parameters:
            cConfigName (str): Name of configuration.
            cNumberOfQuestions (str): The number of questions for each quiz.
            cIsAAndB (str): Whether or not to have A's and B's.
            cRandAB (str): Whether or not A's and B's are random.
            cSameAB (str): Whether or not A's and B's are the same as numbered question.
            cTypeMinMax (array of arrays of str): Min and Max data for configuration.
        """

        self.configName = cConfigName
        self.numberOfQuestions = cNumberOfQuestions
        self.isAAndB = cIsAAndB
        self.randAB = cRandAB
        self.sameAB = cSameAB
        self.typeMinMax = cTypeMinMax


class ConfigList:
    """
    A class to store the config files and perform operations on it.

    Attributes:
        configFileNames (array of str): An array to store config filenames.
        configList (array of config objects): An array to store the config data.
    """

    configFileNames = ["default.csv"] # The array that stores all of the config filenames
    configList = [] # The array of config data objects

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

        # Ensure that the program config exists, if not make it
        try:
            configFile = open(configFileName, 'r')
        except IOError:
            configFile = open(configFileName, 'w')
        configFile.close()

        # Read in filenames for config files
        configFile = open(configFileName, "r")
        for line in configFile:
            line.rstrip()
            self.configFileNames.append(line)
        configFile.close()

        # Read in Config data from each file
        for fileName in self.configFileNames:
            file = open(fileName, "r")
            line1 = (file.readline()).rstrip()
            line1 = line1.split(",")
            typeMinsAndMaxs = []
            for line in file:
                line = line.rstrip()
                typeMinsAndMaxs.append(line.split(","))
            self.configList.append(Config(fileName[:-4], line1[0], line1[1], line1[2], line1[3], typeMinsAndMaxs))
            file.close()

    def printConfigData(self):
        """
        Function to print config data.
        """

        for config in self.configList:
            print("=====================================")
            print("Config Data for: " + config.configName)
            print("Number of Questions: " + config.numberOfQuestions)
            print("Are there A'[s and B's: " + config.isAAndB)
            if config.randAB == "1" and config.sameAB == "0":
                aBType = "Random"
            elif config.sameAB == "1" and config.randAB == "0":
                aBType = "Same as numbered question"
            else:
                print(config.randAB)
                print(config.sameAB)
                aBType = "Error!!!"
                print("File Error!!!")
            print("A's and B's question type: " + aBType)
            print("     Min,  Max")
            print("Ma:   " + config.typeMinMax[0][0] + ",    " + config.typeMinMax[0][1])
            print("CR:   " + config.typeMinMax[1][0] + ",    " + config.typeMinMax[1][1])
            print("CVR:  " + config.typeMinMax[2][0] + ",    " + config.typeMinMax[2][1])
            print("Q:    " + config.typeMinMax[3][0] + ",    " + config.typeMinMax[3][1])
            print("FTV:  " + config.typeMinMax[4][0] + ",    " + config.typeMinMax[4][1])
            print("SIT:  " + config.typeMinMax[5][0] + ",    " + config.typeMinMax[5][1])
            print("=====================================")

    # def exportConfigFiles(self, configFileName): # CDL=> To be implemented
    #     """
    #     Function to export config data.
    #
    #     Parameters:
    #         configFileName (str): The output file name of program config data.
    #     """