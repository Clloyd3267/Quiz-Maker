import time

# Project Imports
from QuizMaker import *


if __name__ == "__main__":
    qM = QuizMaker()

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

    qM.numQuestions = int(input("How many questions do you want? (20 or 30) "))
    print("")

    while True:
        refRange = input("What is the range of material? "
                         "(Press Enter for all the material or 'h' for help on setting the material range) ")
        if refRange == "":
            refRange = ["John,1,1-John,21,25"]
            break
        elif refRange == "h":
            print("\nEnter the material ranges in the format: 'BOOK,CHAPTER,VERSE-BOOK,CHAPTER,VERSE' "
                  "Enter as many of these ranges separated by a comma. \n"
                  "Example: 'John,1,1-John,21,25' \n\n")
        else:
            refRange = refRange.split()
            break

    print("")
    numQuizzes = int(input("How many quizzes do you want to generate? "))

    print("Running")
    start_time = time.time()
    qM.generateQuizzes(numQuizzes, refRange)
    print("Done in {:.2f}s".format(time.time() - start_time))