import time

# Project Imports
from QuizMaker import *

def runProgram(qM):

    numQuizzes = 0
    refRanges = []
    filename = ""

    # Print Header
    print("######################################################")
    print("#   ____              __  __          _              #")
    print("#  / __ \      (_)   |  \/  |   /\   | |             #")
    print("# | |  | |_   _ _ ___| \  / |  /  \  | | _____ _ __  #")
    print("# | |  | | | | | |_  / |\/| | / /\ \ | |/ / _ \ '__| #")
    print("# | |__| | |_| | |/ /| |  | |/ /__\ \|   <  __/ |    #")
    print("#  \_____/\____|_/___|_|  |_/_/    \_\_|\_\___|_|    #")
    print("######################################################")
    print("")
    print("C&MA Bible Quizzing Quiz Maker (V01) by Chris Lloyd and Andrew Southwick.")
    print("For more details visit: https://github.com/Clloyd3267/Quiz-Maker")
    print("Email Chris Lloyd with any questions, comments, or bugs: Legoman3267@gmail.com")
    print("")
    print("######################################################")
    print("Type 'q' at anytime to quit the program")
    print("Type 'r' at anytime to re-run the program")
    print("######################################################")

    # Num questions loop
    while True:
        print("")
        userInput = input("How many questions do you want? (20 or 30) ")
        if userInput.lower() == "q":
            return 1
        if userInput.lower() == "r":
            return 2

        if userInput.isnumeric():
            qM.numQuestions = int(userInput)
            if qM.numQuestions == 20 or qM.numQuestions == 30:
                break
        print("Invalid input! Must be either 20 or 30.")

    # Ref range loop
    while True:
        print("")
        userInput = input("What is the range of material? "
                          "(Press Enter for all the material or 'h' for help on setting the material range) ")

        if userInput.lower() == "q":
            return 1
        if userInput.lower() == "r":
            return 2
        if userInput.lower() == "h":
            print("\nEnter the material ranges in the format: 'BOOK CHAPTER:VERSE-BOOK CHAPTER:VERSE' "
                  "Enter as many of these ranges separated by a comma. \n"
                  "Example: 'John 1:2-John 1:4, John 1:6-John 2:3' \n\n")
            continue

        if userInput == "":
            refRanges = ["John 1:1-John 21:25"]
        else:
            refRanges = userInput.split(",")

        # Remove leading and trailing spaces
        refRanges = [range.strip() for range in refRanges]

        # Remove duplicate spaces
        refRanges = [' '.join(range.split()) for range in refRanges]

        # Remove spaces around "-" and ":"
        refRanges = [range.replace(" -", "-") for range in refRanges]
        refRanges = [range.replace("- ", "-") for range in refRanges]
        refRanges = [range.replace(" :", ":") for range in refRanges]
        refRanges = [range.replace(": ", ":") for range in refRanges]

        # Replace ":", and " " with ","
        refRanges = [range.replace(":", ",") for range in refRanges]
        refRanges = [range.replace(" ", ",") for range in refRanges]
        break

    # Num quizzes loop
    while True:
        print("")
        userInput = input("How many quizzes do you want to generate? ")
        if userInput.lower() == "q":
            return 1
        if userInput.lower() == "r":
            return 2

        if not userInput.isnumeric():
            print("Invalid input! Must be a number.")
        else:
            numQuizzes = int(userInput)
            break

    # Filename Selector
    print("")
    print("File going to documents.")
    userInput = input("What would you like to name this quiz set? ")
    if userInput.lower() == "q":
        return 1
    if userInput.lower() == "r":
        return 2
    filename = userInput

    # Run the program
    print("Running")
    start_time = time.time()
    qM.generateQuizzes(numQuizzes, refRanges, filename)
    print("Done in {:.2f}s".format(time.time() - start_time))

    # Done loop
    while True:
        print("")
        userInput = input("Quizzes generated! Would you like to quit 'q' or re-run 'r' the program? ")
        if userInput.lower() == "q":
            return 1
        if userInput.lower() == "r":
            return 2


if __name__ == "__main__":
    qM = QuizMaker()

    # Main program loop
    while True:
        status = runProgram(qM)
        if status == 1:
            print("Exiting!")
            break
        elif status == 2:
            print("\n" * 1000)
            continue
