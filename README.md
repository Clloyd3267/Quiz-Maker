# Quiz-Maker
Python program used for creating C&amp;MA Bible Quizzing quizzes.

#### About
This program is designed to assist in building quizzes for C&MA Bible Quizzing from a chosen question set.

### Getting Started

#### Prerequisites
This project is built using Python 3.6, Xlxswriter, Openpyxl, and Tkinter. Ensure you have them installed and working properly from the links below:

* (https://www.python.org/downloads/release/python-365/)
* (http://xlsxwriter.readthedocs.io/)
* (https://openpyxl.readthedocs.io/en/stable/)
* (https://wiki.python.org/moin/TkInter)

You can also install the packages using [Pip](https://pip.pypa.io/en/latest/quickstart/#quickstart):

* pip install xlsxwriter
* pip install openpyxl
* pip install tkinter

#### Input files
The program requires two data files in order to run. Both should be stored in the "Data Files" folder.

One is an Excel document containing the material called "Verses.xlsx". It should have the following columns (with headers):
* Book => The Book name of verse.
* Chapter => The Chapter number of verse.
* Verse => The Verse number of verse.
* Verse Text => The actual Verse Text.

The other one is an Excel document containing the desired question set called "Questions.xlsx". It should have the following columns (with headers):
* Book => The Book name of question.
* Chapter => The Chapter number of question.
* Verse Start => The start Verse number of question.
* Verse End => The end Verse number of question.
* Type => the type of question.
* Question => The actual question.
* Answer => The answer to the question.

#### Running the program
To run the program, first enter the number of quizzes. Then enter the material ranges in the format: "BOOK,CHAPTER,VERSE-BOOK,CHAPTER,VERSE". Enter as many of these ranges separated by a comma. Once you have entered this information click the generate quizzes button. It will then ask for the output file name and location.
```
ListMaker.py
```
#### Author(s)
* **Chris Lloyd** - *Main Program* - Legoman3267@Gmail.com
* **Andrew Southwick** - *Gui Design*

