###################################################################################################
# Name        : QuizMaker.py
# Author(s)   : Chris Lloyd
# Description : A file to test Python things
###################################################################################################
def foo(x, y, z):
    return
    # print("First is ", x, " then ", y, " lastly ", z)


a = [1, 50, 99]

# foo(a)
# TypeError: foo() takes exactly 3 arguments (1 given)

foo(*a)
# First is 1 then 50 lastly 99

b = [[55, 66, 77], 88, 99]
foo(*b)
# First is [55,66,77] then 88 lastly 99

d = {"y": 23, "z": 56, "x": 15}

foo(*d)
# This passes in the keys of the dict
# First is z then x lastly y

a = [72]
print(*a)